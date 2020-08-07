index.html: README.md style.css
	pandoc --standalone --css style.css $< -o $@

methodology.html: methodology.md style.css
	pandoc --standalone --css style.css $< -o $@
