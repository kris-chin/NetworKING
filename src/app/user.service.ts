import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  constructor(
    private http : HttpClient,
  ) { }

  login(loginData){
    //logs in to the flask server, if it's a valid login, returns validated login values to save in a cookie.
    return this.http.post<any>('http://127.0.0.1:5000/login', loginData);
  }

  getGraphData(validatedLoginData){
    //called using data recieved from cookies created from the validated login data
    return this.http.post<any>('http://127.0.0.1:5000/graph', validatedLoginData);
  }
}
