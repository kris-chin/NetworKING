import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm;
  graphData; //move this

  constructor(
    private formBuilder : FormBuilder, 
    private user : UserService,
    private router : Router,
  ) { 
    this.loginForm = this.formBuilder.group({
      user_or_email: null,
      pass: null
    });
  }

  ngOnInit() {

  }

  onSubmit(loginData){
    //submit a post request to the server, subscribe and wait for a response
    this.user.establishSession(loginData)
      .subscribe( //on post response
        (result) => {
          this.graphData = result;
        }
      ).add( //after post response
        () => {
          if (this.graphData != undefined){
            if (this.graphData.success == true){ //SUCCESSFUL LOGIN
              console.log("Successfully logged in as \"" + this.graphData.user.username + "\"");
              
              //update the session's graph data
              this.user.setData(this.graphData);
              this.router.navigateByUrl('graph');
              //graphdata variable is automatically cleared on navigation

            } else { //FAILED LOGIN
              console.log("Failed to log in: Invalid Credentials");
            
            }
          } else { //UNDEFINED LOGIN (shouldn't happen) 
            console.log("Failed to log in: Undefined");
          
          }
          console.log(this.graphData);
        }
      );

    this.loginForm.reset();
  }

}
