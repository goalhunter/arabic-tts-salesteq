# arabic-tts-salesteq
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}

\geometry{margin=1in}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{codepurple},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codegreen},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}

\lstset{style=mystyle}

\title{Arabic TTS Comparison System}
\author{Installation and Usage Instructions}
\date{\today}

\begin{document}

\maketitle

\section{System Overview}
A Streamlit application for comparing Arabic Text-to-Speech engines across different dialects.

\section{Installation Instructions}

\subsection{Prerequisites}
\begin{itemize}
    \item Python 3.8 or higher
    \item pip (Python package installer)
\end{itemize}

\subsection{Setup Process}
Follow these commands to set up the application environment:

\begin{lstlisting}[language=bash, caption=Installation commands]
# Clone the repository (or download the files)
git clone https://github.com/yourusername/arabic-tts.git
cd arabic-tts

# Create a virtual environment
python -m venv tts-env

# Activate the virtual environment
# On Windows:
tts-env\Scripts\activate
# On macOS/Linux:
source tts-env/bin/activate

# Install dependencies
pip install -r requirements.txt
\end{lstlisting}

\subsection{Configuration}
Create a \texttt{.env} file in the project root directory with your API keys:

\begin{lstlisting}
# Azure Speech API
AZURE_API_KEY=your_azure_key_here
AZURE_REGION=eastus

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_key_here
\end{lstlisting}

\section{Usage Instructions}

\subsection{Starting the Application}
Run the following command to start the Streamlit application:

\begin{lstlisting}[language=bash]
# Start the Streamlit app
streamlit run app.py
\end{lstlisting}

The application will be available at: \url{http://localhost:8501}

\subsection{Stopping the Application}
Press \texttt{Ctrl+C} in the terminal to stop the Streamlit server.

\subsection{Deactivating the Virtual Environment}
When you're finished using the application, deactivate the virtual environment:

\begin{lstlisting}[language=bash]
# Deactivate the virtual environment
deactivate
\end{lstlisting}

\end{document}
