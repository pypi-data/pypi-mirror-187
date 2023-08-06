# Example workflow


## Load ontology
via github link or local directory

```python
import ontopics as ot
onthology = ot.load_onthology("https://github.com/OpenCS-ontology/OpenCS")

# or 

onthology = ot.load_onthology("onthologies/OpenCS", objects = "", descriptions = "")
```

## Prepare topics for classification

```python
# topics is a 
topics = onthology.prepare_topics()

```

## Classify text to ontologies

```python
from ontopic.models import TopicalClassifier

text = "In this paper we introduce novel NLP NER machine learning model"
model = TopicalClassifier()

# to get top 10 topics, 5 is by default
topics = model.predict(text, top=10)

# to get topics which are above given threshold of 'probability'
topics = model.predict(text, threshold=0.2)

# to get topics and also probabilities
topics, proba = model.predict(text, proba=True)
```
