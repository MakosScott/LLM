
# imports 
import urllib.request # Extensible library for opening URLs
import re # Regular expression library for string manipulation

url = ("https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch02/01_main-chapter-code/the-verdict.txt") #website URL

file_path = "the-verdict.txt" #name of the file which will be saved locally
urllib.request.urlretrieve(url, file_path) #download the file from the URL and save it locally with the specified file name

with open("the-verdict.txt", "r", encoding="utf-8") as f: #open the file in read mode with UTF-8 encoding
    rawtext = f.read() #read the contents of the file and save them to rawtext variable
print("Total number of character:", len(rawtext))
print(rawtext[:99])

#start of tokenization 


 #split the text into tokens based on whitespace'. r' is used to treat the string as a raw string (for \ to be treated literally). (\s) means any whitespace chraracter. 
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', rawtext)
preprocessed = [item.strip() for item in preprocessed if item.strip()] #remove leading and trailing whitespace from each token and filter out empty tokens
print(len(preprocessed)) #print the number of tokens
print(preprocessed[:30]) #print first 30 tokens just for visual check.

#now that we have tokenized the rawtext, we want to create a aphabetically sorted list of unique tokens. Which will then be assigned an Token ID.
allwords = sorted(set(preprocessed)) #create a sorted list of unique tokens (set() is used to guarantee uniqueness.)
vocab_size = len(allwords) #calculate the vocabulary size (number of *unique* tokens)
print("Vocabulary size:", vocab_size) #print the vocabulary size

#creating the vocabulary
vocab = {token:integer for integer, token in enumerate(allwords)} #create a dictionary mapping each unique token to a unique integer ID using a dictionary comprehension and the enumerate function
print("First 50 items in the vocabulary, with ID:") #print the first 50 items in the vocabulary to check the mapping
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break 

#We now begin the process of creating the tokenizer class.
class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab #store the provided vocabulary mapping from string to integer as an instance variable called str_to_int
        self.int_to_str = {i: s for s, i in vocab.items()} #create a reverse mapping from integer to string using a dictionary comprehension

    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text) #split the input text into tokens using the same regular expression as before
                                                                     # if item.strip() returns FALSE if the string is empty or contains only whitespace, and TRUE otherwise. 
        preprocessed = [item.strip() for item in preprocessed if item.strip()] #remove leading and trailing whitespace from each token and filter out empty tokens
        ids = [self.str_to_int[s] for s in preprocessed] #convert each token to its corresponding integer ID using the str_to_int mapping
        return ids
    
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids]) #join the list of tokens into a single string with spaces in between
        text = re.sub(r'\s([,.:;?_!"()\']|--)\s', r'\1', text) #remove spaces around punctuation marks using a regular expression substitution
        return text
    
#Example of tokenization using encode()
tokenizer = SimpleTokenizerV1(vocab) #create an instance of the SimpleTokenizerV1 class with a vocabulary mapping from string to integer
text = """"It's the last he painted, you know," Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text) #encode the input text into a list of integer IDs using the encode method of the tokenizer
print("List of IDs for each tokenized word in the text : """"It's the last he painted, you know,"Mrs. Gisburn said with pardonable pride.""" "") #print a message indicating that the following output is the tokenized list of IDs
print(ids) #print the tokenized list (will be in numeric form)


#now we will decode the list of IDs back into text using the decode() method of the tokenizer
print("Decoded text:") #print a message indicating that the following output is the decoded text
print(tokenizer.decode(ids)) #decode the list of integer IDs back into text using the decode method of the tokenizer

#As the output showed, we could encode and decode the text successfully. Now we will obseve what happens when we try to encode a text that contains a token that is not in our vocabulary.
# text = "Hello, do you like tea?"
# print(tokenizer.encode(text)) #running this line return an error. KeyError: 'Hello' because the token "Hello" is not in our vocabulary, which means that the tokenizer does not know how to convert it into an integer 

#WE will now create a tokenizer that can handle out-of-vocabulary (OOV) tokens and Endoftext tokens. 
all_tokens = sorted(list(set(preprocessed))) #create a sorted list of unique tokens from the preprocessed text
all_tokens.extend(["<|endoftext|>", "<|unk|>"]) #add special tokens for end of text and out-of-vocabulary to the list of all tokens
vocab = {token:integer for integer, token in enumerate(all_tokens)} #create a dictionary mapping each unique token (including special tokens) to a unique integer ID.

print(len(vocab.items())) #print the size of the new vocabulary (which should be larger than before due to the addition of special tokens) which is no 1130 +2 for the two new special tokens.