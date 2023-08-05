import string
import tensorflow_hub as hub
from nltk.corpus import stopwords
from nltk import download as nltk_download
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class Strimilarity():
    """ Class with functions for calculating the similarity between a
        pair or multiple sentences. This class uses vectorization and 
        tokenization, along cosine similarity to calculate the 
        similarity.
    """
    
    def __init__(self, language='en'):
        """ Initialize class

        Args:
            language (str, optional): language for stopwords. Defaults 
                to 'en'.
        """
        
        # Tokenization model
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
        self.model = hub.load(module_url)
        
        # Language selection
        self.available_languages = {
            'en': 'english',
            'es': 'spanish'
        }
        self.current_language = self.available_languages[language]
        
        # Download stopwords
        nltk_download('stopwords')
        
    def clean_string(self, text):
        """ Returns string in lower case and  without stopwords or
            punctiotion.

        Args:
            text (str): text to clean.

        Returns:
            str: cleaned text.
        """
        
        # Get stopwords of the current language
        stops = stopwords.words(self.current_language)
        
        # Remove punctuation and stopwords
        text = text.lower()
        text = ''.join([w for w in text if w not in string.punctuation])
        text = ''.join([w for w in text if w not in stops])
        
        # Return clean text
        return text
    
    def similarity(self, sentences, w_lexical = 1, w_semantic = 1):
        """ Returns a matrix representing the avarage of the lexicals
            and semantics similarities, represented as percentages
            from 0-1, between all the sentences.

        Args:
            sentences (list): 1d list of strings with the sentences to
                compare.
            w_lexical (int, optional): weight for the lexical similarity
                used in calculating the weighted avarage between lexical
                and semantic similarities. Defaults to 1.
            w_semantic (int, optional): weight for the semantic 
                similarity used in calculating the weighted avarage 
                between lexical and semantic similarities. Defaults to 1.

        Returns:
            np.array: array representing the similarities between all
                the sentences.
        """
        
        # Raise error due insuficient sentences
        if len(sentences) < 2:
            raise 'Error. More than 1 sentence is required.'
        
        # Raise error due weights error
        if w_lexical <= 0 or w_semantic <= 0:
            raise 'Error. One or more of the weights is equal or less than 0. \
                Weights greater than 0 are required.'
        
        # Get lexical and semantic similarities matrixes
        sim_lex = self.lexical_similarity(sentences)
        sim_sem = self.semantic_similarity(sentences)
        
        # Calculate weighted avarage matrix
        w = w_lexical + w_semantic
        sim_avg = (sim_lex * w_lexical + sim_sem * w_semantic) / w
        
        # Return similarity between sentences
        return sim_avg
    
    def similarity_pair(self, sentence1, sentence2, w_lexical = 1, 
                        w_semantic = 1):
        """ Return the avarage of the lexical and semantic similarity
            between two sentences represented as a percentage from 0-1.

        Args:
            sentence1 (str): First sentence to compare.
            sentence2 (str): Second sentence to compare.
            w_lexical (int, optional): weight for the lexical similarity
                used in calculating the weighted avarage between lexical
                and semantic similarities. Defaults to 1.
            w_semantic (int, optional): weight for the semantic 
                similarity used in calculating the weighted avarage 
                between lexical and semantic similarities. Defaults to 1.

        Returns:
            float: percentage form 0-1 representing the similarity
                between both sentences.
        """
        
        # Get matrix of similarities
        similarity_matrix = self.similarity([sentence1, sentence2], w_lexical, 
                                            w_semantic)
        
        # Return similarity between sentence1 vs sentence 2
        return similarity_matrix[0][1]
    
    def lexical_similarity(self, sentences):
        """ Returns a matrix representing the lexicals similarities, 
            represented as percentages from 0-1, between all the 
            sentences.

        Args:
            sentences (list): 1d list of strings with the sentences to
                compare.

        Returns:
            np.array: array representing the similarities between all
                the sentences.
        """
        
        # Raise error due insuficient sentences
        if len(sentences) < 2:
            raise 'Error. More than 1 sentence is required.'
        
        # Clean text
        cleaned_text = list(map(self.clean_string, sentences))
        
        # Vectorize texts
        vectorizer = CountVectorizer().fit_transform(cleaned_text)
        vectors = vectorizer.toarray()
        
        # Get cosine similarity
        similarity_matrix = cosine_similarity(vectors)
        
        # Return similarity between sentences
        return similarity_matrix
    
    def lexical_similarity_pair(self, sentence1, sentence2):
        """ Returns the lexical similarity between two sentences 
            represented as a percentage from 0-1.

        Args:
            sentence1 (str): First sentence to compare.
            sentence2 (str): Second sentence to compare.

        Returns:
            float: percentage form 0-1 representing the similarity
                between both sentences.
        """
        
        # Get matrix of similarities
        similarity_matrix = self.lexical_similarity([sentence1, sentence2])
        
        # Return similarity between sentence1 vs sentence 2
        return similarity_matrix[0][1]
    
    def semantic_similarity(self, sentences):
        """ Returns a matrix representing the semantical similarities, 
            represented as percentages from 0-1, between all the 
            sentences.

        Args:
            sentences (list): 1d list of strings with the sentences to
                compare.

        Returns:
            np.array: array representing the similarities between all
                the sentences.
        """
    
        # Raise error due insuficient sentences
        if len(sentences) < 2:
            raise 'Error. More than 1 sentence is required.'
        
        # Clean text
        cleaned_text = list(map(self.clean_string, sentences))
        
        # Embed texts
        embeddings = self.model(cleaned_text)
        
        # Get cosine similarity
        similarity_matrix = cosine_similarity(embeddings)
        
        # Return similarity between sentences
        return similarity_matrix
    
    def semantic_similarity_pair(self, sentence1, sentence2):
        """ Returns the semantical similarity between two sentences 
            represented as a percentage from 0-1.

        Args:
            sentence1 (str): First sentence to compare.
            sentence2 (str): Second sentence to compare.

        Returns:
            float: percentage form 0-1 representing the similarity
                between both sentences.
        """
        
        # Get matrix of similarities
        similarity_matrix = self.semantic_similarity([sentence1, sentence2])
        
        # Return similarity between sentence1 vs sentence 2
        return similarity_matrix[0][1]
        
        
        