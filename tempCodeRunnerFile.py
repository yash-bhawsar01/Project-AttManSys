
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            roll_no = student_ids[matchIndex]
            if roll_no not in marked_students:
                marked_students.add(roll_no)

                # Get the current date in 'YYYY-MM-DD' format