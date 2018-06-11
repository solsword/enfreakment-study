" Open test file
tabe hits.csv
3
"49

" Yank id1 and go back to other tab
normal yt,f,l
tabp
" Replace all
exe "%s`\\${id1}`" . @" . "`g"

" Tab, yank name1, tab
tabn
normal yt,f,l
tabp
" Replace all
exe "%s`\\${name1}`" . @" . "`g"

" shortname1
tabn
normal yt,f,l
tabp
" Replace all
exe "%s`\\${shortname1}`" . @" . "`g"

" namepossessive1
tabn
normal yt,f,l
tabp
exe "%s`\\${namepossessive1}`" . @" . "`g"

" etc.
tabn
normal yt,f,l
tabp
exe "%s`\\${imageA1}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageB1}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageC1}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${country1}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gender1}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gendergroup1}`" . @" . "`g"
" Bio is quoted w/ no escaped quotes inside:
tabn
normal lyt"f"ll
tabp
exe "%s`\\${bio1}`" . @" . "`g"
" Quote is the same
tabn
normal lyt"f"ll
tabp
exe "%s`\\${quote1}`" . @" . "`g"


" And now character #2:
tabn
normal yt,f,l
tabp
exe "%s`\\${id2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${name2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${shortname2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${namepossessive2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageA2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageB2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageC2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${country2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gender2}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gendergroup2}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${bio2}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${quote2}`" . @" . "`g"

" #3:
tabn
normal yt,f,l
tabp
exe "%s`\\${id3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${name3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${shortname3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${namepossessive3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageA3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageB3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageC3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${country3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gender3}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gendergroup3}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${bio3}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${quote3}`" . @" . "`g"

" #4:
tabn
normal yt,f,l
tabp
exe "%s`\\${id4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${name4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${shortname4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${namepossessive4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageA4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageB4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageC4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${country4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gender4}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gendergroup4}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${bio4}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${quote4}`" . @" . "`g"

" #5:
tabn
normal yt,f,l
tabp
exe "%s`\\${id5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${name5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${shortname5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${namepossessive5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageA5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageB5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${imageC5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${country5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gender5}`" . @" . "`g"
tabn
normal yt,f,l
tabp
exe "%s`\\${gendergroup5}`" . @" . "`g"
tabn
normal lyt"f"ll
tabp
exe "%s`\\${bio5}`" . @" . "`g"
" Note that we can't use f"ll here because that would prevent the gT
tabn
normal lyt"
tabp
exe "%s`\\${quote5}`" . @" . "`g"

" close the extra tab
tabn
q!

" we're done!
