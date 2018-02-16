" Force % to correctly match HTML tags even without loading .vimrc:
packadd matchit
runtime ftplugin/html.vim
" Jump to first character div:
normal /div.*single_character
" Copy entire div into buffer 'a':
normal V%j"ay
" Paste a copy after itself:
normal l%j"ap
" Rewrite 1} to 2} and _1" to _2" in the copy:
normal lV%:s/1}/2}/g
normal gv:s/_1"/_2"/g
" Now jump to next initial </div
normal /^<\/divj
" And repeat the paste/revise process for copies 3, 4, and 5:
normal "ap
normal lV%:s/1}/3}/g
normal gv:s/_1"/_3"/g
normal /^<\/divj
normal "ap
normal lV%:s/1}/4}/g
normal gv:s/_1"/_4"/g
normal /^<\/divj
normal "ap
normal lV%:s/1}/5}/g
normal gv:s/_1"/_5"/g
normal /^<\/divj
" Editing done
