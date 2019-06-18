from pydub import AudioSegment
from random import shuffle
import random
from numpy.random import choice


def concatenate(song_list):
    result = song_list[0]

    for song_part in song_list[1:]:
        result += song_part

    return result


def concatenate_with_style(song_list):

    result = song_list[0]

    for song_part in song_list[1:]:
        probability = random.randint(0, 1)
        if probability > 0.9:
            result.append(song_part, crossfade=len(song_part)/4)
        else:
            result += song_part

    return result


def divide_it_by_sec(song, step):
    #print("dividing, step: " + str(step))
    result = []

    for i in range(step,len(song), step):
        result.append(song[i-step: i])
        #deletes the last part --change this

    return result


def mix_me(song_section, level=0):
    #print("mixing")

    result = []

    mix_type = ["nothing", "reverse", "louder", "quieter"]

    if level==0:
        probabilities = [0.4, 0.3, 0.15, 0.15]
    else:
        probabilities = [0.1, 0.3, 0.3, 0.3]

    shuffle(song_section)

    for section in song_section:
        #do_what = choice(mix_type, p=probabilities)

        probability = random.randint(0, 1)
        if probability<0.25:
            count = random.randint(2, 4)
        else:
            count= 1

        while count>0:
            do_what = choice(mix_type, p=probabilities)
            if do_what=="nothing":
               result.append(section)
            elif do_what=="reverse":
               result.append(section.reverse())
            elif do_what=="louder":
                result.append(section + 3)
            else: # do_what=="quieter":
                result.append(section - 3)
            count -=1


    return result


def by_quarter(original_song):

    length = len(original_song)

    print("length is ", length)

    first_quarter = original_song[:length / 4]
    second_quarter = original_song[length / 4:length / 2]
    third_quarter = original_song[length/2: length* 3/4]
    fourth_quarter = original_song[-length/4:]

    #lists
    first_quarter = divide_it_by_sec(first_quarter, 3000)
    second_quarter = divide_it_by_sec(second_quarter, 1000)
    third_quarter = divide_it_by_sec(third_quarter, 500)
    fourth_quarter = divide_it_by_sec(fourth_quarter, 2000)

    new_song = []

    new_song.extend(mix_me(first_quarter))
    new_song.extend(mix_me(second_quarter))
    new_song.extend(mix_me(third_quarter))
    new_song.extend(mix_me(fourth_quarter))

    return concatenate_with_style(new_song)

def symphonize_it(original_song):
    length = len(original_song)

    print("length is ", length)

    first_third = original_song[:length / 3]
    second_third = original_song[length / 3:-length / 3]
    third_third = original_song[-length/3:]

    #lists
    first_third = divide_it_by_sec(first_third, 2000)
    second_third = divide_it_by_sec(second_third, 800)
    third_third = divide_it_by_sec(third_third, 1000)

    new_song = []

    new_song.extend(mix_me(first_third))
    new_song.extend(mix_me(second_third, 1))
    new_song.extend(mix_me(third_third))

    return concatenate_with_style(new_song)

def mix_two(original_song1, original_song2):
    combine = by_quarter(original_song1) + by_quarter(original_song2)
    combination = mix_me(divide_it_by_sec(combine, 4000))
    return concatenate_with_style(combination)

def main(file_name1, file_name2):
    try:
        original_song1 = AudioSegment.from_file(file_name1, "m4a")
        original_song2 = AudioSegment.from_file(file_name2, "m4a")

        mixed_song = symphonize_it(original_song1)

        mixed_both_songs = mix_two(original_song1, original_song2)

        mixed_song.export("mixedversion.mp4", format="mp4")
        mixed_both_songs.export("doublemixedversion.mp4", format="mp4")

    except FileNotFoundError:
        print("File not found.")

if __name__ == '__main__':
    main("sample1.m4a", "sample2.m4a")