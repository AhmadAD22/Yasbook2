
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $subject = $_POST["subject"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // Replace the following line with the appropriate mail() function call
    $to = "yasafco@gmail.com"; // Replace with your actual email address
    $subject = "New Contact Form Submission";

    // Customize the email body as per your requirements
    $body = "Name: $name\n";
    $body .= "Subject: $subject\n";
    $body .= "Email: $email\n";
    $body .= "Message: $message";

    // Send the email
    $success = mail($to, $subject, $body);

    if ($success) {
        echo "Success";
    } else {
        http_response_code(500);
        echo "Error: Unable to send email";
    }
} else {
    http_response_code(400);
    echo "Error: Invalid request";
}
?>
