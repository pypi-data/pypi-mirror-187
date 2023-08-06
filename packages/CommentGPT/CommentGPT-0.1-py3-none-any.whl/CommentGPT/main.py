import os, sys, getopt
from CommentGPT import commenter as c


section_size = 50  # How many lines compose each chunk of code sent to ChatGPT
testing_mode = False


def get_args():
    argv = sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:tc:", ["ifile=", "ofile=", "test", "chunk-size="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--test"):
            global testing_mode
            testing_mode = True
        elif opt in ("-c", "--chunk-size"):
            global section_size
            section_size = arg

    if inputfile != '':
        inputfile = inputfile.strip() # trim the leading & trailing spaces
    else:
        inputfile = argv[-1] # if there's no flag used, the last argument is the input file

    if outputfile != '':
        outputfile = outputfile.strip() # trim the leading & trailing spaces
    else:
        # if no '-o' flag was provided, the output file will be the input file + "_commented
        # (Ex: input.cpp -> input_commented.cpp)
        name, ext = os.path.splitext(inputfile)
        outputfile = name + "_commented" + ext
    return inputfile, outputfile


if __name__=="__main__":
    # get the input file & output file names from the arguments
    inputfile, outputfile = get_args()

    # verify if ChatGPT is working, if requested
    c.verify_connection() if testing_mode else None

    # read in the input file's text
    with open(inputfile) as file:
        snippet= file.read()

    # Actually comment the code & return the commented code
    combined_response = c.comment_code(snippet, section_size)

    # write the commented code to an output file
    with open(outputfile, 'w') as file:
        file.write(combined_response)