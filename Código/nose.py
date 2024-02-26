import cv2

# Main function
def main():
    cap = cv2.VideoCapture(0)  # Open webcam device 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Define the coordinates and size of the fixed rectangle area
        area_x, area_y = 190, 232  # Coordinates of the top-left corner of the area
        area_width, area_height = 180, 110  # Size of the area

        # Draw the fixed rectangle area on the frame
        cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 255, 0), 2)

        # Extract the fixed rectangle area from the frame
        selected_frame = frame[area_y:area_y + area_height, area_x:area_x + area_width]
        selected_frame = cv2.flip(selected_frame, 1)

        frame = cv2.flip(frame, 1)

        # Display the selected area
        cv2.imshow('Selected Area', selected_frame)

        # Display the frame with the fixed rectangle area
        cv2.imshow('Fixed Area', frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()