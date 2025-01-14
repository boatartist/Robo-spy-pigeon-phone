from teachable_machine_lite import TeachableMachineLite

ai = TeachableMachineLite(model_path='letter_identifier.tflite', labels_file_path='labels.txt')

def identify_letter(filename):
    return ai.classify_image(filename, calc_time=False)

if __name__ == '__main__':
    print(identify_letter())