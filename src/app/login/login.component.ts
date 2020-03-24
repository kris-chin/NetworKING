import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm;

  constructor(
    private formBuilder : FormBuilder, 
    private user : UserService,
    private router : Router,
    private cookieService: CookieService,
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
    let validationResponse;
    this.user.login(loginData)
      .subscribe( //on post response
        (result) => {
          validationResponse = result;
        }
      ).add( //after post response
        () => {
          if (validationResponse != undefined){
            if (validationResponse.success == true){ //SUCCESSFUL LOGIN
              console.log("Successfully logged in as \"" + loginData.user_or_email + "\"");
              
              //set the login cookie so you don't have to constantly
              this.cookieService.set('user_validated', validationResponse.user_validated)
              this.cookieService.set('pass_validated', validationResponse.pass_validated)

              this.router.navigateByUrl('graph');

            } else { //FAILED LOGIN
              console.log("Failed to log in: Invalid Credentials");
            
            }
          } else { //UNDEFINED LOGIN (shouldn't happen) 
            console.log("Failed to log in: Undefined");
          
          }
        }
      );

    this.loginForm.reset();
  }

}
