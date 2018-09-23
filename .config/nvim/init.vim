set number
set tabstop=4
set shiftwidth=4
set expandtab
set updatetime=300
filetype plugin indent on
syntax on
" set termguicolors

" NOTE: CTRL+[ is equivalent to ESC
" NOTE: :nnoremap <buffer> <leader> xyz :call SomeFunc(input('Param: '))<CR>
"       will allow you to add parameters to your mappings
let g:mapleader = '"'

" Markdown composer
function! BuildComposer(info)
  if a:info.status != 'unchanged' || a:info.force
    if has('nvim')
      !cargo build --release
    else
      !cargo build --release --no-default-features --features json-rpc
    endif
  endif
endfunction

call plug#begin()

" Plug 'roxma/nvim-completion-manager'  " commented because it autoinserts
" when simply moving across text
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
" Plug 'brooth/far.vim'
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'airblade/vim-gitgutter'
" Plug 'neomake/neomake'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'severin-lemaignan/vim-minimap'

" for development of nvim
Plug 'tweekmonster/nvimdev.nvim'
Plug 'tweekmonster/helpful.vim'

" linting
Plug 'dbakker/vim-lint'
Plug 'w0rp/ale'

" Cpp
" Plug 'Valloric/YouCompleteMe', { 'do': './install.py --clang-completer' }
Plug 'rhysd/vim-clang-format'
Plug 'octol/vim-cpp-enhanced-highlight'

" Javascript
Plug 'jelera/vim-javascript-syntax'
" Plug 'pangloss/vim-javascript'

" buggy
" Plug 'vimlab/neojs'
" autocompletion
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'wokalski/autocomplete-flow'
Plug 'Shougo/neosnippet'
Plug 'Shougo/neosnippet-snippets'
Plug 'Shougo/echodoc.vim'
let g:deoplete#enable_at_startup = 1

" autocmd FileType javascript set formatprg=prettier\ --stdin
"format on save & restore cursor position on save
"autocmd BufWritePre *.js :normal gggqG
"autocmd BufWritePre *.js exe "normal! gggqG\<C-o>\<C-o>"

" Kotlin
Plug 'udalov/kotlin-vim'

" Dart
Plug 'dart-lang/dart-vim-plugin'

" XML
Plug 'othree/xml.vim'
Plug 'gregsexton/MatchTag'

" Solidity
Plug 'tomlion/vim-solidity'

" themes
Plug 'tomasiser/vim-code-dark'
Plug 'joshdick/onedark.vim'

" Latex
" Plug 'lervag/vimtex'
Plug 'donRaphaco/neotex', { 'for': 'tex' }

" Markdown
Plug 'euclio/vim-markdown-composer', { 'do': function('BuildComposer') }

" Typescript
Plug 'mhartington/nvim-typescript'

" Vue
Plug 'posva/vim-vue'

call plug#end()

colorscheme onedark
" vscodeydark
let g:airline_theme = 'onedark'

" Neotex options
let g:neotex_pdflatex_alternative = 'xelatex'

let g:ale_max_signs = 500

let g:gitgutter_terminal_reports_focusports_focus=0
let g:gitgutter_max_signs = 500
let g:gitgutter_enabled = 1  " default
let g:gitgutter_signs = 1  " default
let g:gitgutter_highlight_lines = 0  " default
let g:gitgutter_async = 1  " default

let NERDTreeShowHidden=1
" NERDTree commands
map <silent> <C-n> :NERDTreeToggle<CR>

" nvim-completion-manager config
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
" preview windowing
set completeopt-=preview

" tabs
map <C-j>u :tabp<CR>
map <C-j>i :tabn<CR>
map <C-j>n :tabe 

" windows

map <C-w>N :vnew<CR>
" resizing
" NOTE: default mapping is:
" N<C-w>-  = decrease height by N
" N<C-w>+  = increase height by N
" N<C-w><  = decrease width by N
" N<C-w>>  = increase width by N
" N<C-w>_  = set height to N
" N<C-w>|  = set width to N
" N<C-w>=  = equalize width and height of all windows
map <C-w>t :vertical resize -1<CR>
map <C-w>i :vertical resize +1<CR>
map <C-w>y :resize -1<CR>
map <C-w>u :resize +1<CR>

" " Copy to clipboard
" +y is copy letter
" +yy is copy line
" vnoremap  <leader>y  "+y
" nnoremap  <leader>Y  "+yg_
" nnoremap  <leader>y  "+y
" nnoremap  <leader>yy  "+yy

" " Paste from clipboard
" nnoremap <leader>p "+p
" nnoremap <leader>P "+P
" vnoremap <leader>p "+p
" vnoremap <leader>P "+P


" Javascript specifics
au FileType javascript setl sw=2 sts=2 et

" Highlight ES6 template strings
hi link javaScriptTemplateDelim String
hi link javaScriptTemplateVar Text
hi link javaScriptTemplateString String

" js custom colors
" hi jsUndefined guifg=#ff0000 guibg=NONE gui=NONE
" hi jsArrowFunction guifg=#ff0000 guibg=NONE gui=NONE

" general color operators
" hi Operator guifg=#10aaaa guibg=NONE gui=NONE

" Dart specifics
au FileType dart setl sw=2 sts=2 et

" Custom syntax highlighting changes
" Possibly have to set (^[ is single character inserted in vim by <ctrl>-v <esc>
" set t_ZH=^[[3m
" set t_ZR=^[[23m
highlight Comment cterm=italic


let g:minimap_highlight='Visual'
" minimap shortcuts
let g:minimap_show='<leader>ms'
let g:minimap_update='<leader>mu'
let g:minimap_close='<leader>mc'
let g:minimap_toggle='<leader>mm'

