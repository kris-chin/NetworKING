import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  userData;

  constructor(
    private http : HttpClient,
  ) { }

  //sends a POST to the flask server
  //1. establishes a flask session with the user being logged in
  //2. returns graph data of the current user graph
  establishSession(loginData){
    //console.warn(loginData);

    //creates a post request with the given loginData, sets this.userData as the json response
    this.http.post<any>('http://127.0.0.1:5000/graph', loginData).subscribe(result=> this.userData = result);
    
    //console.warn(this.userData);
  }
}
