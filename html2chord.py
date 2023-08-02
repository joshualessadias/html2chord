import glob, os

pathToSource = "D:/Documents/projetos/py-script/source/"
pathToFormatted = "D:/Documents/projetos/py-script/formatted_songs/"
os.chdir(pathToSource)
fileList = glob.glob("*.html")

for file in fileList:
    fileName = file[:-5]

    # open and copy song data
    file = open(pathToSource + file, "r")
    fileData = file.read()
    file.close()

    bracketedSong = fileData

    # replacing wrong characters for the brazilian ones
    bracketedSong = bracketedSong.replace(r'\n', '\n')
    bracketedSong = bracketedSong.replace(r'\u00e3', '\u00e3')
    bracketedSong = bracketedSong.replace(r'\u00e7', '\u00e7')
    bracketedSong = bracketedSong.replace(r'\u00f3', '\u00f3')
    bracketedSong = bracketedSong.replace(r'\u00e9', '\u00e9')
    bracketedSong = bracketedSong.replace(r'\u00c9', '\u00c9')

    # removing html tags
    bracketedSong = bracketedSong.replace('<pre>', '')
    bracketedSong = bracketedSong.replace(r'<\/pre>', '')

    # adding brackets around chords
    bracketedSong = bracketedSong.replace('<strong>', '[')
    bracketedSong = bracketedSong.replace(r'<\/strong>', ']')

    # string broke into an array of each line of the string itself
    lineArray = bracketedSong.splitlines()

    # index of line
    i = 0

    # array of each chord
    chordArray = []

    # store all chords
    for line in lineArray:
        # index of char
        j = 0
        for char in line:
            # found a chord
            if char == '[':
                chordArray.append([i, j])
            j = j + 1
        i = i + 1

    # reversing chords array
    chordArray = chordArray[::-1]

    lastLineIndex = -1

    # move chords down
    for chord in chordArray:
        i = chord[0] # i: line of the current chord
        j = chord[1] # j: first column of the current chord. Example: if chord is [Cm], j is position of [

        # delete past chords line
        currentLineIndex = i
        if currentLineIndex < lastLineIndex:
            lineArray.pop(lastLineIndex)
        lastLineIndex = currentLineIndex

        char = lineArray[i][j] # first char of the chord ([)
        k = j
        while char != ']': # on final, k is the position of the last character os the chord (])
            k += 1
            char = lineArray[i][k]

        # exclude isolated chords, such as intro chords
        if (len(lineArray[i+1]) > 0):

            chordToBeMovedDown = ''
            for n in range(j, k+1):
                chordToBeMovedDown += lineArray[i][n]

            lineLen = len(lineArray[i+1])

            # if chord is far front from the line below
            if j > lineLen:
                spacesToBeAdded = j - lineLen
                spaces = ''
                while spacesToBeAdded > 0:
                    spaces = spaces + ' '
                    spacesToBeAdded -= 1
                lineArray[i+1] = lineArray[i+1] + spaces + chordToBeMovedDown
            else:
                lineArray[i+1] = lineArray[i+1][:j] + chordToBeMovedDown + lineArray[i+1][j:]
        else:
            lastLineIndex = -1

            # add spaces between chords in isolated chords, such as intro
            lineArray[i] = lineArray[i][:k] + '     ' + lineArray[i][k:]

    # mark words in isolated chords lines
    lineIndex = 0
    while lineIndex < len(lineArray):
        isChord = 0
        isOpened = 0
        columnIndex = 0
        if len(lineArray) > lineIndex + 1 and len(lineArray[lineIndex + 1]) == 0 and (len(lineArray[lineIndex - 1]) == 0 or  lineIndex == 0):
            while columnIndex < len(lineArray[lineIndex]):
                # chord ending
                if isChord and lineArray[lineIndex][columnIndex] == ']':
                    isChord = 0
                elif isChord == 0:
                    # chord beginning
                    if lineArray[lineIndex][columnIndex] == '[':
                        isChord = 1
                    # beginning of random word
                    elif isOpened == 0 and lineArray[lineIndex][columnIndex] != ' ':
                        lineArray[lineIndex] = lineArray[lineIndex][:columnIndex] + '[' + lineArray[lineIndex][columnIndex:]
                        isOpened = 1
                    elif isOpened == 1:
                        # ending of random word
                        if lineArray[lineIndex][columnIndex] == ' ':
                            lineArray[lineIndex] = lineArray[lineIndex][:columnIndex + 1] + ']' + lineArray[lineIndex][columnIndex + 1:]
                            columnIndex += 1
                            isOpened = 0
                        # ending of line when opened brackets
                        elif columnIndex == len(lineArray[lineIndex]) - 1:
                            lineArray[lineIndex] = lineArray[lineIndex] + ']'
                            columnIndex += 1
                columnIndex += 1
        lineIndex += 1

    finalSong = '\n'.join(lineArray)

    print(finalSong)

    formattedFileName = pathToFormatted + fileName + ".txt"
    try:
        newFile = open(formattedFileName, "x", encoding = "utf-8-sig")
    except:
        print('\nDuplicated file will be replaced\n')
        newFile = open(formattedFileName, "w", encoding = "utf-8-sig")
    finally:
        newFile.write(finalSong)
        newFile.close