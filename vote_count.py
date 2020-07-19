num_candidates = int(input('How amny candidates will compete? '));
candidates = list(input() for _ in range(num_candidates));
print(candidates);
print('Here are the candidates : ');
print('\n'.join(candidates));
chosen_candidates = [];
votes = [];
people_in_line = 'y';
cast_vote = 'y';
while people_in_line == 'y':
    chosen_candidate = input('Please enter a candidate you choose from the list ');
    if chosen_candidate in candidates:
        chosen_candidates.append(chosen_candidate);
    else:
        print('Sorry! Your vote will not count.');
        cast_vote = 'n';
    print('Thank you for participating in this voting');
    people_in_line = input('Are there any people in line? ');

# count votes
votes = list(0 for _ in range(num_candidates));
print(votes);
for person in chosen_candidates:
    candidate_index = candidates.index(person);
    votes[candidate_index] += 1;
print(votes);
# max votes count
max_votes = 0;
max_candidate = [];
for i in range(len(votes)):
    if votes[i] > max_votes:
        max_votes = votes[i];
        max_candidate.append(candidates[i]);
    elif votes[i] == max_votes:
        max_candidate.append(candidates[i]);
print('TAhe highest votes goes to :');
print('\n'.join(max_candidate));
print(f'He/she/They got {max_votes} votes');



