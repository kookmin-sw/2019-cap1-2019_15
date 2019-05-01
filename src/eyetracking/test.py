def hanoi(n, start, mid, end) :
	if(n==1):
		print("{} : {} -> {}".format(n,start,end))

	else :
		hanoi(n-1,start,end,mid)
		print("{} : {} -> {}".format(n, start, end))
		hanoi(n-1,mid,start,end)



hanoi(3,'A','B','C')