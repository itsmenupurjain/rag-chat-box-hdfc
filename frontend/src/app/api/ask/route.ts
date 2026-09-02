import { NextRequest, NextResponse } from 'next/server';
import Groq from 'groq-sdk';
import { fundChunks } from './fund-data';

// --- Refusal & Greeting Handlers ---
const advisoryPatterns = [
  /should i invest/i, /is it good to invest/i, /which (fund|scheme) is better/i,
  /best (fund|scheme)/i, /recommend/i, /suggest a (fund|scheme)/i,
  /where to invest/i, /is this a good (fund|scheme)/i, /predict/i,
  /future returns/i, /how much return will i get/i,
];

const greetingPatterns = [
  'hi', 'hello', 'hey', 'h', 'hola', 'greetings',
  'hi there', 'hello there', 'hey there',
];

function isAdvisory(query: string): boolean {
  return advisoryPatterns.some((p) => p.test(query));
}

function isGreeting(query: string): boolean {
  const clean = query.toLowerCase().trim().replace(/[^a-z0-9 ]/g, '');
  if (greetingPatterns.includes(clean)) return true;
  if (clean.includes('how are you') || clean.includes('how are u')) return true;
  return false;
}

// --- Simple keyword search (replaces TF-IDF on the server) ---
function retrieveContext(query: string, k = 8) {
  const queryWords = query.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(/\s+/).filter(Boolean);

  const scored = fundChunks.map((chunk) => {
    const text = chunk.content.toLowerCase();
    let score = 0;
    for (const word of queryWords) {
      if (text.includes(word)) score++;
    }
    // Bonus for scheme name match
    const scheme = chunk.scheme.toLowerCase();
    for (const word of queryWords) {
      if (scheme.includes(word)) score += 2;
    }
    return { ...chunk, score };
  });

  return scored
    .filter((c) => c.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, k);
}

// --- LLM Generation ---
// Models (updated Sept 2026 — llama-3.3-70b-versatile was deprecated by Groq)
const PRIMARY_MODEL = 'qwen/qwen3.8-27b';
const FALLBACK_MODEL = 'allam-2-7b';

const SYSTEM_PROMPT = `You are a facts-only mutual fund FAQ assistant. Your role is to provide 
accurate, verifiable information about mutual fund schemes using ONLY 
the provided context from official sources.

RULES:
1. Answer ONLY using information from the provided context.
2. If the information is not in the context, say: "I'm sorry, but I don't have that specific information in my current records."
3. Maximum 3 sentences per response.
4. Include EXACTLY ONE source citation link from the context at the end.
5. NEVER provide investment advice, recommendations, or personal opinions.
6. NEVER say "I recommend", "You should", "This is better", or "I think".
7. Be concise, factual, and precise.
8. Do NOT include any thinking, reasoning, or internal monologue tags in your response.`;

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json();

    if (!query || typeof query !== 'string') {
      return NextResponse.json({ response: 'Please provide a valid query.' }, { status: 400 });
    }

    // 1. Greeting check
    if (isGreeting(query)) {
      return NextResponse.json({
        response:
          'Hello! I am your HDFC Mutual Fund FAQ Assistant. I can provide you with factual details like NAV, Expense Ratio, and Fund Manager information for HDFC schemes. How can I help you today?',
      });
    }

    // 2. Advisory check
    if (isAdvisory(query)) {
      return NextResponse.json({
        response:
          "I can't provide investment advice or recommendations. My role is to share only factual, publicly available information about mutual fund schemes.\n\nFor investment guidance, you may consult a SEBI-registered financial advisor or visit AMFI's investor education page: https://www.amfiindia.com/investor-awareness\n\nFacts-only. No investment advice.",
      });
    }

    // 3. Retrieve context
    const contextChunks = retrieveContext(query);

    if (contextChunks.length === 0) {
      return NextResponse.json({
        response:
          "I'm sorry, I couldn't find any factual information about that specific query in the HDFC Mutual Fund records I have.",
      });
    }

    // 4. Call Groq LLM
    const apiKey = process.env.GROQ_API_KEY;
    if (!apiKey) {
      return NextResponse.json(
        { response: 'Service configuration error: API key not set.' },
        { status: 503 }
      );
    }

    const groq = new Groq({ apiKey });

    const contextText = contextChunks
      .map((c) => `[Source: ${c.url} | Scheme: ${c.scheme}]\n${c.content}`)
      .join('\n\n');

    const userContent = `Context from official sources:\n${contextText}\n\nUser Query: ${query}\n\nProvide a factual response following all rules.`;

    // Try primary model, then fallback
    const modelsToTry = [PRIMARY_MODEL, FALLBACK_MODEL];
    let response = '';
    let lastError: unknown = null;

    for (const model of modelsToTry) {
      for (let attempt = 1; attempt <= 3; attempt++) {
        try {
          console.log(`Calling Groq (model=${model}, attempt=${attempt}/3)`);
          const completion = await groq.chat.completions.create({
            model,
            messages: [
              { role: 'system', content: SYSTEM_PROMPT },
              { role: 'user', content: userContent },
            ],
            temperature: 0.1,
            max_tokens: 200,
          });

          response = completion.choices[0]?.message?.content || '';

          // Strip <think>...</think> tags some models emit
          if (response.includes('<think>')) {
            response = response.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
          }

          if (response) break;
        } catch (err) {
          lastError = err;
          console.error(`Groq error (model=${model}, attempt=${attempt}):`, err);
          if (attempt < 3) await new Promise((r) => setTimeout(r, 2000 * attempt));
        }
      }
      if (response) break;
    }

    if (!response) {
      console.error('All models/retries exhausted. Last error:', lastError);
      return NextResponse.json(
        { response: 'I encountered an error while generating the response. Please try again later.' },
        { status: 500 }
      );
    }

    // 5. Ensure citation & footer
    const hasUrl = /https?:\/\/\S+/.test(response);
    if (!hasUrl && contextChunks.length > 0) {
      response += `\n\nSource: ${contextChunks[0].url}`;
    }

    const today = new Date().toISOString().split('T')[0];
    response += `\n\nLast updated from sources: ${today}`;

    return NextResponse.json({ response });
  } catch (error) {
    console.error('API route error:', error);
    return NextResponse.json(
      { response: 'An internal error occurred. Please try again later.' },
      { status: 500 }
    );
  }
}
