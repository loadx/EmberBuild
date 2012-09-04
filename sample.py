from ember import EmberBuild

def main():
	EmberBuild('testapp/app/', 'dev').build_app()	

if __name__ == "__main__":
	main()
