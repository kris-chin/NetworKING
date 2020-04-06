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
  signupForm;

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
    this.signupForm = this.formBuilder.group({
      email: null,
      user: null,
      pass: null
    })
  }

  ngOnInit() {
    let cookieData = {'user_validated': this.cookieService.get('user_validated'), 'pass_validated' : this.cookieService.get('pass_validated')};
    //autoredirect if there are logincookies
    if (cookieData.user_validated != '' && cookieData.pass_validated != '') {
      this.router.navigateByUrl('graph');
    }

  }

  loginSubmit(loginData){
    //submit a post request to the server, subscribe and wait for a response
    let validationResponse = undefined;
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
          this.loginForm.reset();
        }
      );
  }

  signupSubmit(signupData){
    //this validation response is the same as the loginSubmit
    let validationResponse;
    this.user.signup(signupData)
      .subscribe(
        (result) => {
          validationResponse = result;
        }
      ).add(
        () => {
          if (validationResponse != undefined){
            if (validationResponse.success == true){
              console.log("Successfully signed up");
              //also create cookies and automatically log in
              this.cookieService.set('user_validated', validationResponse.user_validated)
              this.cookieService.set('pass_validated', validationResponse.pass_validated)

              this.router.navigateByUrl('graph');
            } else {
              console.log("Failed to Sign up (Server returned failure)");
            }
          } else {
            console.log("Failed to Sign up (Response Undefined)");
          }
        }
      );
  }

}
