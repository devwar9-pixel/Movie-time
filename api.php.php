<?php
header('Content-Type: application/json');
$secret_key = "my_secret_key_123";
$input = json_decode(file_get_contents('php://input'), true);

if (!isset($input['secret']) || $input['secret'] !== $secret_key) {
    echo json_encode(["status" => "error", "message" => "Unauthorized"]);
    exit();
}

$file = 'movies.json';
$current_data = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

$new_movie = [
    "id" => time() + rand(10, 99),
    "title" => $input['title'] ?? 'New Movie Release',
    "quality" => $input['quality'] ?? 'HD / Hindi Dubbed',
    "poster" => $input['poster'] ?? 'https://via.placeholder.com/300x450?text=PRMovie',
    "embed_link" => $input['embed_link'] ?? '', // Site ke andar direct play karne ke liye
    "telegram_link" => $input['telegram_link'] ?? '#', // Download / Telegram button ke liye
    "date" => date("Y-m-d H:i")
];

array_unshift($current_data, $new_movie);
file_put_contents($file, json_encode($current_data, JSON_PRETTY_PRINT));
echo json_encode(["status" => "success", "message" => "Movie added successfully!"]);
?>