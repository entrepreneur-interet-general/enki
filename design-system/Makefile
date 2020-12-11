deploy:
	parcel build index.html
	git checkout main
	git add .
	git commit -m "Deployment to heroku..."
	cd .. &&	git subtree push --prefix="design-system/dist" heroku main