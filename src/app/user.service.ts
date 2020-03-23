import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { timingSafeEqual } from 'crypto';

@Injectable({
  providedIn: 'root'
})

export class UserService {
  graphData;

  constructor(
    private http : HttpClient,
  ) { }

  //sends a POST to the flask server
  //1. establishes a flask session with the user being logged in
  establishSession(loginData){
    //creates a post request with the given loginData.
    //returns an observable that becomes json data.
    //todo: turn this into sessiondata
    return this.http.post<any>('http://127.0.0.1:5000/graph', loginData);
  }

  //access graph data if the user is logged in.
  //returns observable
  accessSession(){
    return this.http.get('http://127.0.0.1:5000/graph');
  }

  //sets the user graphData to the inputted graph data.
  setData(data){
    this.graphData = data;
  }
}
