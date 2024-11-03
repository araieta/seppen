from PyPDF2 import PdfReader
import re
import json
import os

def get_pdf_content(filename):
    reader = PdfReader(filename)
    pagesn = len(reader.pages)
    page = reader.pages[0]
    data = ""
    text = page.extract_text()
    for ctn in range(1,pagesn):
        data += reader.pages[ctn].extract_text()
    return data

def extract_questions_content(text):
    """Estrae le domande, le scelte e le spiegazioni dal testo fornito e restituisce un dizionario."""
    pattern = r'NEW QUESTION \d+\s*(.*?)\n([A-D]\.\s*.*?)(?=\nExplanation:\s*(.*?)\nNEW QUESTION \d+|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    questions_dict = {}
    
    for index, match in enumerate(matches, start=1):
        question_text = match[0].strip()
        choices = re.findall(r'([A-D])\.\s*(.*)', match[1])
        
        # Estrai le scelte
        choice_list = [choice[1].strip() for choice in choices]
        
        # La risposta corretta è la prima scelta indicata
        answer = choices[0][0] if choices else None
        
        # Estrai l'explanation
        explanation = match[2].strip() if len(match) > 2 else ""
        
        questions_dict[str(index)] = {
            "Question": question_text,
            "Choice": choice_list,
            "Answer": answer,
            "Explanation": explanation
        }
    
    return questions_dict


def main():
    #load filename from target folder
    target_folder = 'C:\\Users\\andre\\Desktop\\SPLK-2003'
    file_list = None
    data = []
    try:
        file_list = os.listdir(target_folder)
        print(f"* File List: {file_list}")
        for filename in file_list:
            print(f"* Process file {filename}")
            #extract pdf content
            txt_tmp = get_pdf_content(os.path.join(target_folder,filename))
            print(f"\t * extract pdf content")
            ext = extract_questions_content(txt_tmp)
            print(f"\t * extract question content from txt format")
            data.append(ext)
            print(f"\t * append in dict of List")
            print(f"\t* Process file {filename} Done")
            print('#################### \n')
        
    except:
        print('files list wrong.')
    
    print('* Write on file json')
    with open('test.json', 'w') as f:
        f.write( str(data) )

if __name__ == "__main__":
    main()