<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ImageController;

Route::post('/scan', [ImageController::class, 'scan']);
Route::get('/image/view', [ImageController::class, 'view']);
Route::post('/image/delete', [ImageController::class, 'delete']);
