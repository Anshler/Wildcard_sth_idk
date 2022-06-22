import glob
import numpy as np
import string

search_query = 'chicken'
HASH_BASE = 9973
HASH_MODE = 1000000007
hash_func = None
doc_content = None
pow_base = None


class SearchEngine2:
    def __init__(self):
        self.file_dir = self.getDirDocument()

    def getDirDocument(self):
        DOCUMENT_DIRECTION = ".\\Document"
        return glob.glob(DOCUMENT_DIRECTION + "\\*.txt")

    def processingQuery(self, search_query):
        query = list()
        word = ""
        for character in search_query:
            if character != '*' and character != '?':
                word += character
                continue

            if len(word) > 0:
                query.append(word)
                word = ""

            query.append(character)

        if len(word) > 0:
            query.append(word)

        return query

    def calHashQuery(self, query_index):
        hash_query = 0
        for character in query[query_index]:
            hash_query = int((hash_query * HASH_BASE + ord(character)) % HASH_MODE)

        return hash_query

    def searchInContent(self):
        queue = list()
        # query index, content index, is continuous
        queue.append((0, 1, False))
        num_result = 0
        while (len(queue) > 0):
            status = queue.pop(0)
            query_index = status[0]
            content_index = status[1]
            is_continuos = status[2]

            if query_index >= len(query):
                # print(content_index)
                num_result += 1
                continue

            if query[query_index] == '*':
                queue.append((query_index + 1, content_index, False))
                continue

            if content_index >= len(doc_content):
                continue

            max_len = len(doc_content)
            if is_continuos == True:
                max_len = content_index + 1

            if query[query_index] == '?':
                for l_index in range(content_index, max_len):
                    if doc_content[l_index] in string.ascii_letters:
                        queue.append((query_index + 1, l_index + 1, True))

            hash_query = self.calHashQuery(query_index)

            len_query = len(query[query_index])

            for l_index in range(content_index, max_len + 1):
                r_index = len_query + l_index - 1
                if r_index > len(doc_content) - 1:
                    break

                hash_lr = (hash_func[r_index] - hash_func[l_index - 1] * pow_base[
                    r_index - l_index + 1] + HASH_MODE * HASH_MODE) % HASH_MODE

                if hash_lr == hash_query:
                    queue.append((query_index + 1, r_index + 1, True))

        return num_result

    def readContent(self, directory):
        file_handler = open(directory, 'r', encoding='utf-8')
        doc_content = file_handler.read()
        file_handler.close()
        return doc_content

    def searchPerDocument(self, directory):
        file_handler = open(directory, 'r', encoding='utf-8')
        global doc_content
        doc_content = file_handler.read()
        file_handler.close()
        doc_content = "$" + doc_content

        # calculate hash function for doc content
        global hash_func
        hash_func = np.zeros(len(doc_content))
        hash_func = hash_func.astype(np.longlong)
        for id, character in enumerate(doc_content):
            if id == 0:
                continue
            hash_func[id] = int((hash_func[id - 1] * HASH_BASE + ord(character)) % HASH_MODE)

        global pow_base
        pow_base = np.zeros(len(doc_content))
        pow_base = pow_base.astype(np.longlong)
        pow_base[0] = 1
        for i in range(1, len(doc_content)):
            pow_base[i] = int((pow_base[i - 1] * HASH_BASE) % HASH_MODE)

        return directory, self.searchInContent()

    def __call__(self, search_query):
        global query
        query = self.processingQuery(search_query=search_query)
        # print(query)
        query_in_page = list()
        for file in self.file_dir:
            dir, num_results = self.searchPerDocument(file)
            if num_results > 0:
                query_in_page.append([dir, num_results, str(dir.split("\\")[-1])])

        return query_in_page

# engine = SearchEngine()
# results = engine('*a*')
# total_results = 0
# print(results)
# for result in results:
#     total_results += result[1]

# print('Total: ',total_results)