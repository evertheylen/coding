==========================
 Coding Theory, in Python
==========================

Content
=======

This is a Python implementation of (parts of) the `"Codetheorie" course at UAntwerpen <https://www.uantwerpen.be/popup/opleidingsonderdeel.aspx?catalognr=1001WETCOD&taal=nl&aj=2015>`_, given by Stijn Symens.

Since there is also a project throughout the year concerning the "old" crypto part (Vigenère, Enigma, ...) of the course, this project will not try to implement that (chapters 1 and 2). Instead it focuses on the other chapters:

0. Finite fields: **TODO**

1. (Introduction etc: skipped)

2. (Enigma: skipped)

3. Discrete logarithm: **TODO**

4. RSA: **TODO**

5. Rijndael: **TODO**

6. Error correcting codes: **TODO**

7. Linear codes: **TODO**

8. Perfect codes: **TODO**

9. Cyclic codes: **TODO**

10. BCH codes: **TODO**

11. Reed-Solomon codes: **TODO**
  
The implementation focusses on elegance, and performance is of almost no concern. The code itself is of great value here, and not just the functionality it provides.


Notebooks
=========

To use and experiment with the code, I use Jupyter. However, I don't want output in the git, so I use `nbstripout <https://github.com/kynan/nbstripout>`_ to strip that away. You may have to install it when committing (``pip install nbstripout``), as it is set up as a git filter. If you'd rather not install Jupyter, Github has excellent support for viewing Jupyter notebooks. You can copy paste the parts you want into a normal Python terminal.


Support
=======

*There is only one version, the latest version.* I make full use of the glorious f-strings, so Python 3.6 or newer is required.
