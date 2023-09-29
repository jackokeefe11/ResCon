import tkinter as tk
from tkinter import ttk
from annoy import AnnoyIndex
import cohere
from cohere.responses.classify import Example
import numpy as np
from dotenv import load_dotenv
import os 

load_dotenv()

lab_descriptions = [
    "Specializing in the intricate world of genetic engineering, NeuroGen is at the forefront of research on neurodegenerative diseases.",
    "Pioneering the crossroads between AI and biological imaging, the AI Visionary Research Center bridges gaps and opens new horizons.",
    "Dedicated to understanding the ramifications of climate change, the Marine Climate Studies Lab delves deep into marine ecosystems.",
    "Pushing the boundaries of chemistry, the Organic Synthesis Hub is all about creating therapeutic compounds for the future.",
    "Where computational methods meet neuroscience, the Brain Computation Unit investigates the digital representation of neural processes.",
    "Understanding the depths of our gut, the MicroBiome Insight Lab focuses on the intricate balance of the human microbiome.",
    "Exploring the nuances of quantum mechanics, QuantumLife Research Group seeks biotechnological applications of quantum theories.",
    "Bridging medicine and mechanics, RoboMed Innovations is redefining surgical procedures with state-of-the-art robotics.",
    "Where mathematical theories meet biology, the MathBio Modeling Center is all about predicting and analyzing biological systems.",
    "With a keen eye on drug delivery, PharmaTarget Laboratory is revolutionizing how targeted therapies are administered.",
    "Interpreting human movement through an engineering lens, Biomech Engineering Lab explores biomechanics like never before.",
    "Diving deep into DNA sequences, Genome Informatics Group stands at the cusp of personalized medicine with its bioinformatics expertise.",
    "From viruses to bacteria, the Infectious ImmunoLab is decoding the mysteries of the immune response to emerging diseases.",
    "Unlocking secrets from the past, the Ancient DNA Analysis Unit delves into genetics of ancient and extinct populations.",
    "Combining genetics and agriculture, AgriGen Tech Lab is pioneering sustainable and advanced farming methods.",
    "Where aerospace meets medicine, AeroMed Devices Center designs innovative devices inspired by aviation principles.",
    "Diving deep into the human mind, CogBias Psychological Studies is unraveling cognitive biases and decision-making processes.",
    "Studying the planet's heartbeat, GeoImpact Environmental Lab researches the consequences and solutions to environmental disruptions.",
    "Connecting diet to health, NutriMolecular Research Group is at the cutting edge of understanding diet-induced diseases.",
    "Peering into the universe's origins, CosmoGenesis Astronomy Unit explores the cosmic beginnings and life's interstellar possibilities."
]

lab_names = [
        "NeuroGen",
        "AI Visionary Research Center",
        "Marine Climate Studies Lab",
        "Organic Synthesis Hub",
        "Brain Computation Unit",
        "MicroBiome Insight Lab",
        "QuantumLife Research Group",
        "RoboMed Innovations",
        "MathBio Modeling Center",
        "PharmaTarget Laboratory",
        "Biomech Engineering Lab",
        "Genome Informatics Group",
        "Infectious ImmunoLab",
        "Ancient DNA Analysis Unit",
        "AgriGen Tech Lab",
        "AeroMed Devices Center",
        "CogBias Psychological Studies",
        "GeoImpact Environmental Lab",
        "NutriMolecular Research Group",
        "CosmoGenesis Astronomy Unit"
]

examples = [
    # Examples for NeuroGen
    Example(
        "My recent projects involved studying genetic mutations leading to neurodegenerative diseases. Courses taken: Genetics, Molecular Biology, Neurology",
        lab_descriptions[0]
    ),
    Example(
        "I've been focusing on the genetic aspects of Alzheimer's and Parkinson's. Courses taken: Advanced Genetics, Neurological Studies, Genetic Engineering",
        lab_descriptions[0]
    ),

    # Examples for AI Visionary Research Center
    Example(
        "My research bridges AI algorithms and medical imaging. Courses taken: AI in Medicine, Digital Imaging, Deep Learning",
        lab_descriptions[1]
    ),
    Example(
        "I've developed convolutional networks tailored for biological data interpretation. Courses taken: Computer Vision, Medical Imaging, AI Principles",
        lab_descriptions[1]
    ),

    # Examples for Marine Climate Studies Lab
    Example(
        "I've spent years studying the effects of global warming on marine life. Courses taken: Marine Biology, Climate Science, Ecosystem Analysis",
        lab_descriptions[2]
    ),
    Example(
        "My interest lies in understanding how marine ecosystems adapt to changing climatic conditions. Courses taken: Environmental Science, Oceanography, Conservation Biology",
        lab_descriptions[2]
    ),
    # Examples for the Organic Synthesis Hub
    Example(
        "I've been deeply involved in creating new organic compounds that have therapeutic potential. Courses taken: Organic Chemistry, Medicinal Chemistry, Molecular Design",
        lab_descriptions[3]
    ),
    Example(
        "Synthesizing novel organic molecules for future medicinal applications has been the crux of my research. Courses taken: Organic Synthesis, Drug Design, Chemical Biology",
        lab_descriptions[3]
    ),

    # Examples for the Brain Computation Unit
    Example(
        "My studies focus on the intricate dance between computational methods and understanding the neural processes. Courses taken: Neuroscience, Computational Biology, Neural Data Analysis",
        lab_descriptions[4]
    ),
    Example(
        "I am passionate about creating computational models that can mimic and predict neural behaviors. Courses taken: Computational Neuroscience, Machine Learning, Brain Informatics",
        lab_descriptions[4]
    ),
    Example(
        "I've always been keen to understand how gut bacteria influences our health. Courses taken: Microbiology, Human Biology, Gut Flora Studies",
        lab_descriptions[5]
    ),
    Example(
        "My research has revolved around the human gut and the world of bacteria within. Courses taken: Microbiology, Nutrition, Disease Studies",
        lab_descriptions[5]
    ),

    # Examples for the QuantumLife Research Group
    Example(
        "The quantum world and its applications in biotech have always fascinated me. Courses taken: Quantum Mechanics, Molecular Biology, Quantum Biology",
        lab_descriptions[6]
    ),
    Example(
        "I've been working on projects that explore the use of quantum mechanics in biology. Courses taken: Quantum Physics, Biochemistry, Quantum Computation",
        lab_descriptions[6]
    ),

    # Examples for RoboMed Innovations
    Example(
        "The idea of combining medicine with robotics to enhance surgical precision is enthralling. Courses taken: Robotics, Medical Engineering, Surgical Procedures",
        lab_descriptions[7]
    ),
    Example(
        "I've been keen on integrating advanced robotics into medical practices. Courses taken: Robotics, Medical Studies, Biomechanics",
        lab_descriptions[7]
    ),
    Example(
    "I've always been passionate about applying mathematical models to predict biological phenomena. Courses taken: Mathematical Biology, Systems Biology, Differential Equations",
    lab_descriptions[8]
    ),
    Example(
        "The intersection of math and biology, especially in modeling biological systems, fascinates me. Courses taken: Applied Mathematics, Systems Biology, Computational Modeling",
        lab_descriptions[8]
    ),

    # Examples for the PharmaTarget Laboratory
    Example(
        "Drug delivery systems and their efficiency in targeting specific cells have been my primary area of research. Courses taken: Pharmacology, Molecular Biology, Biomedical Engineering",
        lab_descriptions[9]
    ),
    Example(
        "I've been involved in designing innovative drug delivery mechanisms using nanotechnology. Courses taken: Nanomedicine, Pharmacology, Bioengineering",
        lab_descriptions[9]
    ),

    # Examples for the Biomech Engineering Lab
    Example(
        "The biomechanics of human movement, especially in relation to sports and injuries, has always been my area of interest. Courses taken: Biomechanics, Kinesiology, Mechanical Engineering",
        lab_descriptions[10]
    ),
    Example(
        "I've undertaken projects that study the mechanical aspects of human joints and muscles. Courses taken: Biomechanics, Anatomy, Materials Science",
        lab_descriptions[10]
    ),

    # Examples for the Genome Informatics Group
    Example(
        "Deciphering genetic data and applying informatics to understand DNA sequences are my passion. Courses taken: Bioinformatics, Genetics, Computational Biology",
        lab_descriptions[11]
    ),
    Example(
        "My research revolves around analyzing large genomic datasets to glean insights into genetic variations. Courses taken: Bioinformatics, Genomic Studies, Data Analytics",
        lab_descriptions[11]
    ),

    # Examples for the Infectious ImmunoLab
    Example(
        "I've always been drawn to the study of the immune response, especially in the context of emerging diseases. Courses taken: Immunology, Virology, Bacteriology",
        lab_descriptions[12]
    ),
    Example(
        "Understanding the immune system's response to various pathogens is what I've dedicated my research to. Courses taken: Immunology, Disease Modeling, Cellular Biology",
        lab_descriptions[12]
    ),
    # Examples for the Ancient DNA Analysis Unit
    Example(
        "I've always been fascinated by the genetics of ancient populations, trying to understand our evolutionary history. Courses taken: Genetics, Archaeology, Evolutionary Biology",
        lab_descriptions[13]
    ),
    Example(
        "Decoding the mysteries of the past by analyzing ancient DNA samples is what I've been passionate about. Courses taken: Molecular Biology, Paleogenetics, Anthropology",
        lab_descriptions[13]
    ),

    # Examples for the AgriGen Tech Lab
    Example(
        "Advancing farming methods using modern genetic techniques has been the cornerstone of my research. Courses taken: Agricultural Science, Genetics, Crop Physiology",
        lab_descriptions[14]
    ),
    Example(
        "With a background in both agriculture and genetics, I aim to pioneer sustainable and advanced farming techniques. Courses taken: Genetics, Agrobiotechnology, Plant Breeding",
        lab_descriptions[14]
    ),

    # Examples for the AeroMed Devices Center
    Example(
        "I'm passionate about designing innovative medical devices, drawing inspiration from aerospace principles. Courses taken: Aerospace Engineering, Medical Device Design, Biomechanics",
        lab_descriptions[15]
    ),
    Example(
        "Combining the principles of aviation with medical technology is where I see the future of medical devices. Courses taken: Biomedical Engineering, Aerospace Design, Robotics",
        lab_descriptions[15]
    ),

    # Examples for the CogBias Psychological Studies
    Example(
        "I have always been intrigued by the ways in which our inherent cognitive biases shape our decisions. Courses taken: Cognitive Psychology, Behavioral Economics, Decision Science",
        lab_descriptions[16]
    ),
    Example(
        "My research focuses on understanding the subtle cognitive biases that affect our everyday judgment. Courses taken: Neuropsychology, Cognitive Science, Behavioral Analysis",
        lab_descriptions[16]
    ),

    # Examples for the GeoImpact Environmental Lab
    Example(
        "Passionate about the environment, I've dedicated my studies to understanding both the consequences of and solutions to ecological disruptions. Courses taken: Environmental Science, Geology, Climate Studies",
        lab_descriptions[17]
    ),
    Example(
        "With a background in geology and environmental science, I'm committed to researching the profound impacts of environmental changes. Courses taken: Earth Sciences, Climate Change, Conservation",
        lab_descriptions[17]
    ),

    # Examples for the NutriMolecular Research Group
    Example(
        "My academic journey revolves around understanding the molecular connections between diet and prevalent diseases. Courses taken: Nutritional Science, Molecular Biology, Metabolic Studies",
        lab_descriptions[18]
    ),
    Example(
        "I've been delving deep into the molecular intricacies that link our dietary habits to health outcomes. Courses taken: Dietetics, Molecular Genetics, Biochemistry of Nutrition",
        lab_descriptions[18]
    ),

    # Examples for the CosmoGenesis Astronomy Unit
    Example(
        "With a longing gaze towards the stars, I've dedicated my studies to uncovering the mysteries of the cosmos, especially the origins of the universe. Courses taken: Astrophysics, Cosmology, Stellar Evolution",
        lab_descriptions[19]
    ),
    Example(
        "My passion lies in exploring the vastness of space, deciphering the cosmic beginnings, and understanding interstellar possibilities. Courses taken: Astronomy, Galactic Studies, Quantum Mechanics",
        lab_descriptions[19]
    )
]

coheres=os.getenv("API_KEY")
print(coheres)

co = cohere.Client(coheres)


def text_to_embedding(text):
    response = co.embed(texts=[text], model='small')
    embeddings = response.embeddings[0]
    return np.array(embeddings)


lab_embeddings = [text_to_embedding(description) for description in lab_descriptions]


def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


def match_student_to_labs(student_info, lab_embeddings, lab_names):
    student_embedding = text_to_embedding(student_info)
    similarities = [cosine_similarity(student_embedding, lab_embedding) for lab_embedding in lab_embeddings]
    
    # Get the top five indices
    top_indices = np.argsort(similarities)[-5:][::-1]
    top_labs = [lab_names[index] for index in top_indices]
    
    # Joining lab names with a newline character for vertical display
    return "\n".join(top_labs)


def classify_student_match(student_info, examples):
    response = co.classify(
        inputs=[student_info],
        examples=examples
    )

    data = response.classifications[0].labels

    sorted_labs = sorted(data.items(), key=lambda x: x[1].confidence, reverse=True)
    top_five_labs = [lab[0] for lab in sorted_labs[:5]]
    top_five_names = [lab_names[lab_descriptions.index(description)] for description in top_five_labs]

    return top_five_names

def on_submit():
    student_description = text_entry.get("1.0", "end-1c")
    
    if algorithm_var.get() == "Embed":
        best_labs = match_student_to_labs(student_description, lab_embeddings, lab_names)
    else:  # Algorithm is "Classify"
        best_lab_names = classify_student_match(student_description, examples)
        best_labs = "\n".join(best_lab_names)
        
    result_label.config(text=f"Top 5 Recommended Labs:\n{best_labs}")

app = tk.Tk()
app.title("Lab Matcher")
app.configure(bg="#B0B0B0")

style = ttk.Style()
style.configure("TButton", background='SystemButtonFace')
style.configure("Highlight.TButton", background='light pink')

mainframe = ttk.Frame(app, padding="40", relief="ridge", borderwidth=30) 
mainframe.grid(column=0, row=0, padx=50, pady=50)

app_title = ttk.Label(mainframe, text="Lab Matcher", font=('Calibri', 16, 'bold'))
app_title.grid(column=1, row=0, pady=20)

instruction_label = ttk.Label(mainframe, text="Enter your description:")
instruction_label.grid(column=1, row=1, pady=10)

algorithm_label = ttk.Label(mainframe, text="Algorithm: Embed") 
algorithm_label.grid(column=1, row=6, pady=10)

text_entry = tk.Text(mainframe, width=60, height=10, wrap=tk.WORD, font=('Calibri', 12))
text_entry.grid(column=1, row=2, pady=10)

submit_button = ttk.Button(mainframe, text="Submit", command=on_submit, width=20)
submit_button.grid(column=1, row=3, pady=20)

result_label = ttk.Label(mainframe, text="Top 5 Recommended Labs:")  
result_label.grid(column=1, row=4, pady=10)

algorithm_var = tk.StringVar(value="Embed")

def highlight(button):
  # Highlight button

  if button == embed_button:
    algorithm_label.config(text="Algorithm: Embed")
  else:
    algorithm_label.config(text="Algorithm: Classify")

embed_button = ttk.Button(mainframe, text="Embed", command=lambda: [algorithm_var.set("Embed"), highlight(embed_button)])
embed_button.grid(column=0, row=5, pady=5, padx=5)

classify_button = ttk.Button(mainframe, text="Classify", command=lambda: [algorithm_var.set("Classify"), highlight(classify_button)])
classify_button.grid(column=2, row=5, pady=5, padx=5)

highlight(embed_button)
algorithm_label.config(text="Algorithm: Embed")

app.mainloop()