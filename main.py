'''
Put in a UltraBox JSON file (other BeepBox files should work too) into input.json.
It will scan each pitch channel for duplicate patters and return a JSON with all dupes merged.
'''

import json

# load the input file
with open("input.json", "r") as file:
    song = json.load(file)

_EMPTY_PATTERN = {"notes": []}

# loop through each channel
channel_i = 0
for channel in song["channels"]:
    # print("\nChannel " + str(channel_i))
    channel_i += 1

    # this records all patterns that share the same notes
    dupes = {}
    patterns = channel["patterns"]
    for i in range(len(patterns)):
        pattern = patterns[i]
        first_match_i = patterns.index(pattern)
        if i == first_match_i:
            continue

        # the current pattern matches a different one that happens first
        if first_match_i not in dupes:
            # create a new entry for the duped pattern
            dupes[first_match_i] = []
        dupes[first_match_i].append(i)

        # replace the current pattern so that it is empty
        patterns[i] = _EMPTY_PATTERN

    # loop through dupes
    sequence = channel["sequence"]
    for dupe_key in dupes.keys():
        for i in dupes[dupe_key]:
            while True:
                try:
                    # replace dupes with the first occurrence
                    # add 1 because pattern indices start at 0, but sequence indices start at 1
                    sequence[sequence.index(i + 1)] = dupe_key + 1
                except ValueError:
                    # this means there are no more occurences of the dupe
                    break

    # delete empty patterns and update all the numbers so the indexes match up
    new_patterns = []
    new_indices = []
    for old_index, pattern in enumerate(patterns):
        if pattern != _EMPTY_PATTERN:
            new_patterns.append(pattern)
            new_indices.append(old_index)
    channel["patterns"] = new_patterns

    # print("New indices: " + str(new_indices))
    # print("Sequence: " + str(sequence))

    # fix sequence numbers
    # print("Update sequence")
    for i in range(len(sequence)):
        if sequence[i] == 0:
            # if the channel isn't playing a pattern at this point
            continue
        old_index = sequence[i] - 1 # convert to indexing that starts with 0
        new_index = new_indices.index(old_index)
        sequence[i] = new_index + 1
        #print(
        #    "bar " + str(i + 1) + ": "
        #    + "old sequence: " + str(old_index + 1)
        #   + ", old index " + str(old_index)
        #    + " now at " + str(new_index)
        #    + ", sequence pattern: " + str(new_index + 1)
        #)

# dump the new data
with open("output.json", "w") as file:
    json.dump(song, file, indent=4)

print("\nPitch channel pattern duplicates have been removed successfully!")
