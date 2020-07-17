black_list = ['Susan' , 'Robert' , 'Raj' ,'Shaheb' , 'Murtaza'];

student_list = list(input() for _ in range(int(input())));
print(student_list);
while '' in student_list:
  a = student_list.index('');
  print(a);
  print(f'please fill in the empty name:' ,end =' ');
  student_list[a] = input();
  print(student_list);

print(student_list);
white_list = [student for student in student_list if student not in black_list];
print(f'These {len(white_list)} student/s are allowed to graduate and they are/he/she is-');
print('\n'.join(student.capitalize() for student in white_list));