import json
import os
import re
from src.logger import setup_logger

logger = setup_logger("document_processor", "indexing.log")

class DocumentProcessor:
    def __init__(self, chunk_size=800, chunk_overlap=100):
        """
        Implements the Hybrid Semantic + Fixed-size chunking strategy.
        - Semantic: Respects logical boundaries (sections, paragraphs).
        - Fixed-size: Ensures chunks stay within token limits.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_json_to_chunks(self, json_data):
        """
        Converts structured fund data into a list of factual text chunks.
        Since the data is already structured, this acts as 'Semantic' chunking
        by grouping related metrics into logical blocks.
        """
        scheme_name = json_data.get("scheme_name", "Unknown Fund")
        url = json_data.get("url", "")
        fund_data = json_data.get("data", {})
        
        chunks = []
        
        # 1. Overview Section
        overview = f"Overview of {scheme_name}: "
        overview += f"Category: {fund_data.get('category')} ({fund_data.get('sub_category')}). "
        overview += f"Fund Manager: {fund_data.get('fund_manager')}. "
        overview += f"Benchmark: {fund_data.get('benchmark')}."
        
        chunks.append(self._create_chunk(overview, scheme_name, url, "Overview"))
        
        # 2. Financials Section
        financials = f"Financial details for {scheme_name}: "
        financials += f"NAV: {fund_data.get('nav')} (as on {fund_data.get('nav_date')}). "
        financials += f"AUM: {fund_data.get('aum')}. "
        financials += f"Expense Ratio: {fund_data.get('expense_ratio')}. "
        financials += f"Exit Load: {fund_data.get('exit_load')}."
        
        chunks.append(self._create_chunk(financials, scheme_name, url, "Financials"))
        
        # 3. Investment Section
        investment = f"Investment limits for {scheme_name}: "
        investment += f"Minimum SIP: {fund_data.get('min_sip')}. "
        investment += f"Minimum Lumpsum: {fund_data.get('min_lumpsum')}."
        
        chunks.append(self._create_chunk(investment, scheme_name, url, "Investment"))
        
        # 4. Risk Section
        risk = f"The risk profile for {scheme_name} is categorized as {fund_data.get('riskometer')}."
        chunks.append(self._create_chunk(risk, scheme_name, url, "Risk"))
        
        # 5. Analysis Section (Pros/Cons)
        pros = fund_data.get("pros", [])
        if pros:
            chunks.append(self._create_chunk(f"Pros of {scheme_name}: " + " ".join(pros), scheme_name, url, "Analysis"))
            
        cons = fund_data.get("cons", [])
        if cons:
            chunks.append(self._create_chunk(f"Cons of {scheme_name}: " + " ".join(cons), scheme_name, url, "Analysis"))

        return chunks

    def split_text_hybrid(self, text, metadata_template):
        """
        Generalized hybrid chunking for large text documents.
        1. Splits semantically by paragraphs/sections.
        2. Merges small parts into fixed-size chunks with overlap.
        """
        # Split by double newlines or logical separators
        semantic_parts = re.split(r'\n\n|\r\n\r\n', text)
        
        chunks = []
        current_chunk = ""
        
        for part in semantic_parts:
            part = part.strip()
            if not part: continue
            
            # If a single part is too large, force split it
            if len(part) > self.chunk_size:
                if current_chunk:
                    chunks.append(self._create_chunk_from_template(current_chunk, metadata_template))
                    current_chunk = ""
                
                # Fixed-size split with overlap
                for i in range(0, len(part), self.chunk_size - self.chunk_overlap):
                    sub_part = part[i:i + self.chunk_size]
                    chunks.append(self._create_chunk_from_template(sub_part, metadata_template))
            else:
                # Merge logic
                if len(current_chunk) + len(part) < self.chunk_size:
                    current_chunk += "\n" + part if current_chunk else part
                else:
                    chunks.append(self._create_chunk_from_template(current_chunk, metadata_template))
                    # Start new chunk with overlap from previous
                    overlap_text = current_chunk[-(self.chunk_overlap):] if len(current_chunk) > self.chunk_overlap else ""
                    current_chunk = overlap_text + "\n" + part
        
        if current_chunk:
            chunks.append(self._create_chunk_from_template(current_chunk, metadata_template))
            
        return chunks

    def _create_chunk(self, content, scheme, url, section):
        return {
            "content": content,
            "metadata": {
                "scheme": scheme,
                "url": url,
                "section": section,
                "chunk_size": len(content)
            }
        }

    def _create_chunk_from_template(self, content, template):
        metadata = template.copy()
        metadata["chunk_size"] = len(content)
        return {
            "content": content,
            "metadata": metadata
        }

    def process_directory(self, processed_dir):
        all_chunks = []
        for filename in os.listdir(processed_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(processed_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    chunks = self.process_json_to_chunks(data)
                    all_chunks.extend(chunks)
            elif filename.endswith(".txt"):
                # Handle raw text files with hybrid strategy
                filepath = os.path.join(processed_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    template = {"source": filename, "type": "text_doc"}
                    chunks = self.split_text_hybrid(text, template)
                    all_chunks.extend(chunks)
                    
        logger.info(f"Processed {len(all_chunks)} total chunks.")
        return all_chunks
