import os

from pyzotero import zotero

from agent.domain.ports.reference_manager import ReferenceManager
from agent.domain.schemas.paper import Paper


class ZoteroAdapter(ReferenceManager):
    """Adapter for interacting with Zotero API via pyzotero."""

    def __init__(self, library_id: str = None, api_key: str = None, library_type: str = "user"):
        """
        Initialize the ZoteroAdapter.
        """
        self.library_id = library_id or os.getenv("ZOTERO_LIBRARY_ID")
        self.api_key = api_key or os.getenv("ZOTERO_API_KEY")
        self.library_type = library_type or os.getenv("ZOTERO_LIBRARY_TYPE", "user")
        
        if not self.library_id or not self.api_key:
            raise ValueError("Zotero configuration missing (ZOTERO_LIBRARY_ID or ZOTERO_API_KEY).")
            
        self.zot = zotero.Zotero(self.library_id, self.library_type, self.api_key)

    def save_paper(self, paper: Paper) -> str:
        """Convert valid Paper domain object to Zotero item and save it."""
        # 1. Create Template
        template = self.zot.item_template('journalArticle')
        
        # 2. Map Fields
        template['title'] = paper.title
        
        # Authors format in Zotero: [{'creatorType': 'author', 'firstName': 'X', 'lastName': 'Y'}]
        # Our domain currently stores authors as list of strings ["Name Surname"].
        # Simple parsing strategy: Split by last space.
        creators = []
        for auth_name in paper.authors:
            parts = auth_name.strip().split(' ')
            if len(parts) > 1:
                last_name = parts[-1]
                first_name = " ".join(parts[:-1])
            else:
                last_name = parts[0]
                first_name = ""
            creators.append({'creatorType': 'author', 'firstName': first_name, 'lastName': last_name})
            
        template['creators'] = creators
        
        if paper.abstract:
            template['abstractNote'] = paper.abstract
            
        if paper.publication_date:
            template['date'] = str(paper.publication_date)
            
        if paper.doi:
            template['DOI'] = paper.doi
            
        if paper.oa_info and paper.oa_info.oa_url:
            template['url'] = paper.oa_info.oa_url
            
        if paper.publisher:
           template['publicationTitle'] = paper.publisher

        # 3. Create Item
        try:
            resp = self.zot.create_items([template])
            # pyzotero returns dict with 'success' (dict of key=>item) and 'failed'
            
            if resp.get('successful'):
                # Extract the Zotero Item Key
                item_key = list(resp['successful'].keys())[0]
                return f"Saved to Zotero. Item Key: {item_key}"
            elif resp.get('failed'):
                failures = resp['failed']
                raise RuntimeError(f"Zotero save failed: {failures}")
            else:
                return "No items created (Duplicate or unknown error)."
                
        except Exception as e:
            raise RuntimeError(f"Error communicating with Zotero: {str(e)}") from e
