import nltk
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
text = "Charles S. Mahan. Dr. Charlie Mahan is Dean and Professor Emeritus in the College of Public Health at the University of South Florida and The Lawton and Rhea Chiles Center for Healthy Mothers and Babies. He holds a joint appointment as Professor, Department of Obstetrics and Gynecology in the USF College of Medicine."
text += "Our Public Health History in Florida: Interview with Charles S. Mahan'	b'Charles S. Mahan, MD was the second Dean of the University of South Florida College of Public Health (1995-2002). A native of West Virginia, he received his MD degree from Northwestern University and did his residency ... from the University of Florida College of Medicine and loved working in the State Health Office, I was reluctant to consider ..."
text += "USF College of Public Health\xe2\x80\x99s (COPH) Dr. Charles Mahan, former dean and professor emeritus of the COPH, will be honored with the 2021 ASPPH Welch-Rose Award for academic public health service.. The ASPPH Welch-Rose Award recognizes the highest standards of leadership and scholarship in public health and honors individuals who have made significant lifetime contributions to the field of ..."
text += "USF College of Public Health\xe2\x80\x99s (COPH) Dr. Charles Mahan, former dean and professor emeritus of the COPH, will be honored with the 2021 ASPPH Welch-Rose Award for academic public health service. ... From the film festival to Delta Omega to a fun night out, the USF College of Public Health\xe2\x80\x99s presence at the 2019 American Public Health ..."
text += "Dr. Charles Mahan received his MD from Northwestern University Medical School in 1964 and completed his residency at the University of Minnesota in 1965. In this oral history interview, Dr. Mahan describes the experiences that spurred his interest in public health, especially in the areas of family planning, prenatal and postpartum care. He also recounts his recruitment by the state of Florida ..."
#print(text)
tokens = word_tokenize(text)
#print(tokens)

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if not w in stop_words and w != ',' and w != '...' and w != '\xe2\x80\x99s']
print(tokens)

frequency_dist = nltk.FreqDist(tokens)
print(sorted(frequency_dist,key=frequency_dist.__getitem__, reverse=True)[0:50])

