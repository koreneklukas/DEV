from app.api.routes.manager import ApplicationApi

my_app = ApplicationApi()
app = my_app.app
def main():
	my_app.run()

if __name__ == "__main__":
	main()
