from Functions.calculateSign import sign

def pointInTriangle(singlePoint, p1, p2, p3):

	d1 = sign(singlePoint, p1, p2)
	d2 = sign(singlePoint, p2, p3)
	d3 = sign(singlePoint, p3, p1)

	has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0) 
	has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

	return not(has_neg and has_pos)
