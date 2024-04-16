from experta import *


from datetime import datetime
import re  # Importe le module pour les expressions régulières
import os

class Document(Fact):
    """Représente un document avec son nom, contenu et type."""
    pass



class DocumentClassifier(KnowledgeEngine):
    @Rule(Document(content=MATCH.content))
    def classify_document(self, content):
        #print(f"Analyse du contenu : {content[:500]}...")  # Affiche un extrait du contenu pour le débogage
        
        # Utilisation d'expressions régulières pour identifier les mots clés
        if re.search(r'\b(facture|tva)\b', content, re.IGNORECASE):
            print("Facture détectée.")
            self.declare(Document(type='Facture'))
        elif re.search(r'\b(entrée|plat|dessert)\b', content, re.IGNORECASE):
            print("Menu détecté.")
            self.declare(Document(type='Menu'))
        else:
            print("Type de document inconnu.")
            self.declare(Document(type='Autre'))

# Le reste du code reste inchangé

def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def get_file_type_and_date(files):
    engine = DocumentClassifier()
    engine.reset()
    documents = []
    
    for file in files:
        content = read_file_content(file)
        engine.declare(Document(name=file, content=content))
        engine.run()
        file_type = [fact.type for fact in engine.facts.values() if isinstance(fact, Document) and hasattr(fact, 'type')]
        file_date = datetime.fromtimestamp(os.path.getmtime(file))
        documents.append((file, file_type[0] if file_type else 'Inconnu', file_date))
        
    documents.sort(key=lambda x: (x[1], x[2]))  # Tri par type et date
    return documents

# Exemple d'utilisation:
files = ["extractionTesseractOCR", "facture2-nettoye2", "menu1"]  # Assurez-vous que ces fichiers existent
sorted_documents = get_file_type_and_date(files)
for doc in sorted_documents:
    print(doc)
