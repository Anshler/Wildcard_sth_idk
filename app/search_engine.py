import os
import math
import glob

class SearchEngine:
    def __init__(self):
        self.files = self.get_directory()

    def __call__(self,keys):
        return_result=[]
        if (keys.find("**") == -1) and (keys.find(" ") == -1) and keys != "" and (keys.find(",,") == -1):
            keys = keys.split(",")
        else:
            return return_result

        for text_dir in self.files:
            count=0
            text=open(text_dir,'r',encoding="utf8").read()
            output_element=""

            for key in keys:
                result = []  # list các kết quả khả thi
                key_element = self.split_key(key)  # list các element trong từ khóa search sau khi cắt ra ?, *, chữ cái riêng biệt
                word_list = text.split()  # hàm này đơn giản, có thể cần hàm phức tạp hơn

                # chia 2 bước: search theo chữ và search theo ký tự wildcard
                result = self.letters_search(word_list, key_element, result)
                result = self.symbols_search(key_element, result)
                if len(result) != 0:
                    x=len(result)
                    count+=1
                    output_element = output_element+"found "+str(x)+" results for: "+str(key)+"\n"
                    #result ko đụng tới, trừ khi yêu cầu in tất cả đáp án ra thì thêm str(result) vào output_element
            if count!=0:
                output_element = output_element+"file name: "+str(text_dir.split("\\")[-1])+"\ndirectory: "+str(text_dir)+"\n"
                return_result.append(output_element)

        return return_result

    def letters_search(self,word_list, key_element, result):  # xét xem từ này chứa đủ các chữ cái trong key ko
        letters_key = []  # key_element sau khi bỏ ? * chừa lại chữ cái
        for i in key_element:
            if i.find("?") == -1 and i.find("*") == -1:
                letters_key.append(i)
        #ko chữ cái, chỉ dấu * trả số lượng >= dấu ?
        if len(letters_key)==0:
          if key_element[0].find("*") != -1:
            if key_element[0].find("?") == -1:
              return word_list
            for i in word_list:
              if len(i)>=key_element[0].count("?"):
                result.append(i)
            return result
          else: #ko chữ cái, chỉ dấu ? trả số lượng = dấu ?
            for i in word_list:
              if len(i) ==len(key_element[0]):
                result.append(i)
            return result

        # tìm kiếm
        for word in word_list:
            word2 = str(word).lower()  # copy lại word rồi loại bỏ dấu?
            word2=word2[key_element[0].count("?"):]
            word2=word2[:len(word2)-key_element[-1].count("?")]
            for i in range(math.ceil(len(letters_key) / 2)):
                if word2.find(letters_key[i].lower()) == -1:
                    word2 = "**"  # nếu ko thì đánh dấu để skip
                    break
                else:
                    word2 = word2.split(letters_key[i].lower(),1)  # mỗi lần tra nếu ra từ khóa rồi thì cắt để sau này ko bị trùng lặp
                    word2 = word2[1]
                if i != (math.ceil(len(letters_key) / 2) - 1) or len(letters_key) % 2 == 0:
                    if word2.find(letters_key[-(i + 1)].lower()) == -1:
                        word2 = "**"  # nếu ko thì đánh dấu để skip
                        break
                    else:
                        word2 = word2.rsplit(letters_key[-(i + 1)].lower(), 1)
                        word2 = word2[0]

            if word2 != "**":
                result.append(word)
        return result

    def symbols_search(self,key_element, result):  # bước cuối cùng, hoàn thành wild card search
        result2 = []  # biến trả về
        letters_key = []  # key_element sau khi bỏ ? * chừa lại chữ cái
        for i in key_element:
            if i.find("?") == -1 and i.find("*") == -1:
                letters_key.append(i)
        if len(letters_key)==0: #ko có chữ, chỉ dấu
            return result
        if len(key_element)==1: #ko có dấu, chỉ chữ
          for i in result:
            if i.lower()==key_element[0].lower():
              result2.append(i)
          return result2
        # gộp key list lại thành string gốc
        key = ""
        for i in key_element:
            key += i

        # key_element sau khi bỏ chữ cái chừa lại ? *, split(" ") để nếu có chữ cái cuối hoặc đầu sẽ tạo element rỗng, mình để giải thích ở dưới
        for i in letters_key:
            key = key.replace(i, " ")
        symbols_key = key.split(" ")

        # wildcard search
        for word in result:
            symbols_key2 = symbols_key  # copy lại xài để ko ảnh hưởng biến gốc
            word2 = str(word).lower()
            wordz = word2[key_element[0].count("?"):]
            wordz = wordz[:len(wordz) - key_element[-1].count("?")]

            # cắt vị trí có chữ cái trong từ khóa, chừa lại vị trí tương ứng với ? *
            for i in range(math.ceil(len(letters_key) / 2)):
                wordz = wordz.replace(letters_key[i].lower(), " ", 1)
                if i != (math.ceil(len(letters_key) / 2) - 1) or len(letters_key) % 2 == 0:
                    wordz = self.rreplace(wordz, letters_key[-(i + 1)].lower(), " ", 1)

            word2 = word2[:key_element[0].count("?")]+ wordz +word2[len(word2) - key_element[-1].count("?"):]

            word2=word2.split(" ")
            # đoạn này giải thích phức tạp lắm, cứ hiểu là split(" ") để đôi khi dư element rỗng ở đầu hoắc cuối, tùy theo từ khóa
            # nếu ko làm vậy thì từ khóa như *abc sẽ ko trả đủ kết quả, vì ko thể xét phía trước nó có kí tự nào ko (vì kí tự rỗng vẫn tính vào dấu wildcard)
            # sau khi làm vậy rồi, mình phải cắt, nếu ko cắt thì từ khóa như abc sẽ trả dư kết quả giống như *abc vì phía trước có j cũng tính hết
            if key_element[0] != "?" and key_element[0] != "*":  # nếu từ khóa bắt đầu bằng chữ cái
                if symbols_key2[0] == '':
                    symbols_key2.remove("")
                if word2[0] == '':
                    word2.remove("")
            if key_element[- 1] != "?" and key_element[- 1] != "*":  # nếu từ khóa kết thúc bằng chữ cái
                symbols_key2.reverse()       # 4 dòng code này đáng lẽ gọi pop() là xong, nhưng nó cứ bị lỗi (đụng tới stack heap) ko hiểu tại sao :)
                if symbols_key2[0] == '':    #
                    symbols_key2.remove("")  #
                symbols_key2.reverse()       #
                if word2[-1] == "":
                    word2.pop()               # cái này pop() bth ko vấn đề
            word3="" #biến gán tạm thời
            # và sau khi cắt xong, các từ hợp lệ sẽ có cùng kích thước với từ khóa
            if len(word2) == len(symbols_key2):
                for t in range(len(symbols_key2)):  # số lượng chữ ko đc ít hơn số dấu ?
                    if len(word2[t]) < symbols_key2[t].count("?") or (symbols_key2[t].find("*") == -1 and len(word2[t]) != symbols_key2[t].count("?")):
                        word3 = "**"  # đánh dấu để loại ra
                if word3 != "**":
                    result2.append(word)
                word3=""
        return result2

    def split_key(self,b):  # split từ khóa theo chữ cái và ký tự wildcard
        b_list = []
        b=str(b)
        c = ""  # biến tạm thời để gán giá trị
        for i in range(len(b)):
            c = c + b[i]  # mỗi vòng lặp sẽ gán ký tự hiện tại vào chuỗi này
            if i == len(b) - 1:
                b_list.append(c)
                c = ""
            else:
                if ((b[i] == "?" or b[i] == "*") and (b[i + 1] != "?" and b[i + 1] != "*")) or (((b[i] != "?" and b[i] != "*") and (b[i + 1] == "?" or b[i + 1] == "*"))):
                    b_list.append(c)  # đoạn trên, nếu đến cuối hàng, hoặc kí tự sau khác thể loại kí tự hiện tại (ký tự khác so với ?*)
                    c = ""  # thì mình append vào list, clear c đi cho vòng lặp mới
        return b_list

    def rreplace(self,s, old, new, occurrence): #replace nhưng từ dưới lên
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def get_directory(self):
        DOCUMENT_DIRECTION = ".\\Document"
        return glob.glob(DOCUMENT_DIRECTION + "\\*.txt")

#a=SearchEngine()
#list=a(input())
#for b in list:
    #print(b)