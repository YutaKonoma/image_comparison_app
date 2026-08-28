<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ImageController extends Controller
{
    public function scan(Request $request)
    {
        // 1. バリデーション
        $request->validate([
            'path' => 'required|string',
            'threshold' => 'integer|min:0|max:32'
        ]);

        // 2. .envからPython APIのURLを取得 (http://python-api:8000)
        $pythonUrl = env('PYTHON_API_URL') . '/analyze';

        // 3. Pythonへリクエストを送信
        $response = Http::timeout(60)->post($pythonUrl, [
            'folder_path' => $request->path,
            'threshold' => $request->threshold ?? 8,
        ]);

        // 4. 結果を判定してVueに返す
        if ($response->successful()) {
            return response()->json($response->json());
        }

        return response()->json([
            'status' => 'error',
            'message' => 'Python APIとの連携に失敗しました'
        ], 500);
    }

    public function view(Request $request)
    {
        $rawPath = $request->query('path');
        $path = urldecode($rawPath);

        if (class_exists('Normalizer')) {
            $path = \Normalizer::normalize($path, \Normalizer::FORM_C);
        }
        \Log::debug("Checking file: " . $path);

        if (!file_exists($path)) {
            \Log::error("File not found in PHP: " . $path);
            \Log::debug("Reference: " . print_r(array_slice(scandir('/data'), 0, 5), true));
            return response()->json(['error' => 'File not found', 'attempted_path' => $path], 404);
        }
        return response()->file($path);
    }

    public function delete(Request $request)
    {
        $path = $request->path;
        if (file_exists($path)) {
            unlink($path); // 削除
            return response()->json(['status' => 'success']);
        }
        return response()->json(['status' => 'error'], 404);
    }
}
