\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{rapport}[25/03/14 : v1.0 classe appelant les packages nécessaires ainsi que les commandes appropriées]

\LoadClass[a4paper, 11pt]{report}

\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{mathrsfs}%package mathématiques
\RequirePackage{amssymb}%symboles mathématiques
\RequirePackage{makeidx}%index
\RequirePackage{amsmath}
\RequirePackage[top=2.5cm ,bottom=2.5cm ,left=2cm , right=2cm ]{geometry}%marges
\usepackage{listings}
\usepackage{xcolor}
\usepackage{verbatim}
\usepackage{textcomp}
\usepackage{moreverb}
\definecolor{grey}{rgb}{0.95,0.95,0.95}
\lstset{numbers=left, tabsize=1, frame=single, breaklines=false, basicstyle=\ttfamily,
   numberstyle=\tiny\ttfamily, framexleftmargin=13mm, backgroundcolor=\color{grey}, xleftmargin=-10mm}
\RequirePackage[francais]{babel}

\setcounter{tocdepth}{2}
\renewcommand{\contentsname}{Plan :}

\lstset{ %
	backgroundcolor=\color{white},   % choose the background color; you must add \usepackage{color} or \usepackage{xcolor}
	basicstyle=\footnotesize,        % the size of the fonts that are used for the code
	breakatwhitespace=false,         % sets if automatic breaks should only happen at whitespace
	breaklines=true,                 % sets automatic line breaking
	captionpos=b,                    % sets the caption-position to bottom
	commentstyle=\color{blue}, % comment style
	deletekeywords={...},            % if you want to delete keywords from the given language
	escapeinside={\%*}{*)},          % if you want to add LaTeX within your code
	extendedchars=true,              % lets you use non-ASCII characters; for 8-bits encodings only, does not work with UTF-8
	frame=single,                    % adds a frame around the code
	keepspaces=true,                 % keeps spaces in text, useful for keeping indentation of code (possibly needs columns=flexible)
	keywordstyle=\color{blue},     % keyword style
	language=Python,                   % the language of the code
	morekeywords={*,...},            % if you want to add more keywords to the set
	numbers=left,                    % where to put the line-numbers; possible values are (none, left, right)
	numbersep=5pt,                   % how far the line-numbers are from the code
	numberstyle=\tiny,               % the style that is used for the line-numbers
	rulecolor=\color{black},         % if not set, the frame-color may be changed on line-breaks within not-black text (e.g. comments (green here))
	showspaces=false,                % show spaces everywhere adding particular underscores; it overrides 'showstringspaces'
	showstringspaces=false,          % underline spaces within strings only
	showtabs=false,                  % show tabs within strings adding particular underscores
	stepnumber=2,                    % the step between two line-numbers. If it's 1, each line will be numbered
	stringstyle=\color{green},     % string literal style
	tabsize=2,                       % sets default tabsize to 2 spaces
	title=\lstname                   % show the filename of files included with \lstinputlisting; also try caption instead of title
}
