<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/{any?}', function () {
    return view('pada/index');
});
Route::get('/user/{any?}', function () {
    return view('pada/index');
});
Route::get('/admin/{any?}', function () {
    return view('pada/index');
});
Route::get('/admin/user/{any?}', function () {
    return view('pada/index');
});
