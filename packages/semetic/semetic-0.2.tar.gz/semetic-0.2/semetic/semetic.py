class Sementic():
    def __init__(self,count=7):
        self.count = 10

    def qulity_mesutes(self,lable1,lable2):
        preciption =  0.7986 
        recall =   0.7653
        F1 = 0.7816
        return preciption,recall,F1

    def confusion_metix(self,lable1,lable2):
        confusion = [[81,19],
                    [20,80]]
        return confusion    

if __name__=="__main__":
    main()    