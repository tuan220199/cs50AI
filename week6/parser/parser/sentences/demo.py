from nltk.tree import Tree

def main():
	
	VP = Tree("VP",[Tree("V",["saw"]),Tree("NP",["him"])])
	S = Tree('S', [Tree('NP', ['I']), VP])
	
	t = Tree.fromstring("(S (NP I) (VP (V saw) (NP him)))")
	t[2].set_label('X')

	print(len(t))
if __name__ == '__main__':
	main()