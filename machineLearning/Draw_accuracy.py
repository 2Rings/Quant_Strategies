import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8,9,10]
y1 = [0.8125,0.8125,0.8125,0.875,0.8,0.9,0.9,0.9125,0.925,0.9125]
y2 = [0.7593582887700535,0.7593582887700535,0.8181818181818181,0.7914438502673797,0.8181818181818181,0.7593582887700535,0.7593582887700535,0.7540106951871658,0.732620320855615,0.7433155080213903]
plt.title('Accuracy on traning set and test set')
plt.plot(x,y1,'-')
plt.plot(x,y2,'-')
plt.text(9, 0.9, 'traning set')
plt.text(9, 0.75, 'test set')
plt.ylabel('accuracy')
plt.xlabel('Adaboost_rounds')
plt.grid(True)
plt.show()
