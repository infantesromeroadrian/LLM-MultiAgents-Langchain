from rouge_score import rouge_scorer
from sacrebleu.metrics import BLEU
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.sentiment import SentimentIntensityAnalyzer
from textstat import flesch_reading_ease, flesch_kincaid_grade
import nltk


# Descargar recursos necesarios
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')


class EvaluationMetrics:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.bleu = BLEU()
        self.sia = SentimentIntensityAnalyzer()

    def calculate_rouge(self, reference, hypothesis):
        scores = self.rouge_scorer.score(reference, hypothesis)
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }

    def calculate_bleu(self, reference, hypothesis):
        tokenized_ref = [word_tokenize(reference)]
        tokenized_hyp = word_tokenize(hypothesis)
        return self.bleu.corpus_score([tokenized_hyp], [tokenized_ref]).score

    def evaluate_readability(self, text):
        return {
            'flesch_reading_ease': flesch_reading_ease(text),
            'flesch_kincaid_grade': flesch_kincaid_grade(text)
        }

    def evaluate_sentiment(self, text):
        return self.sia.polarity_scores(text)

    def evaluate_coherence(self, text):
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        unique_pos = set([tag for word, tag in pos_tags])
        return len(unique_pos) / len(words)

    def evaluate_informativeness(self, text):
        words = word_tokenize(text)
        named_entities = ne_chunk(pos_tag(words))
        named_entity_count = sum(1 for chunk in named_entities if hasattr(chunk, 'label'))
        return named_entity_count / len(words)

    def evaluate(self, response, reference=None):
        evaluation = {
            'readability': self.evaluate_readability(response),
            'sentiment': self.evaluate_sentiment(response),
            'coherence': self.evaluate_coherence(response),
            'informativeness': self.evaluate_informativeness(response)
        }

        if reference:
            evaluation['rouge_scores'] = self.calculate_rouge(reference, response)
            evaluation['bleu_score'] = self.calculate_bleu(reference, response)

        return evaluation