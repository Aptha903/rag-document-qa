from search import retrieve

res = retrieve("What is a mask in NumPy?", k=3)
for r in res:
    print(r)
    print("-----")