import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../user.service';

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
  ) { 
    this.loginForm = this.formBuilder.group({
      user_or_email: '',
      pass: ''
    });
  }

  ngOnInit() {

  }

  onSubmit(loginData){
    this.user.establishSession(loginData);

    //console.warn(loginData); //just a test to see if the loginform 
    this.loginForm.reset();
  }

}
