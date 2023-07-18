import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  constructor(private fb: FormBuilder, private authService: AuthService) {}

  isRegistered: boolean = false;
  registrationResponse: any = {};

  registrationForm: FormGroup = this.fb.group({
    emailAddress: ['', Validators.required],
    userName: ['', Validators.required],
    userPassword: ['', Validators.required],
    confirmUserPassword: ['', Validators.required],
  });

  handleSubmission(): void {
    this.authService.register(this.registrationForm.value).subscribe({
      next: (response) => {
        this.registrationResponse = response;
        this.isRegistered = true;
      },
      error: (response) => {
        this.registrationResponse.message = response.error.detail;
        this.isRegistered = false;
      },
    });
  }

  ngOnInit(): void {
    this.registrationForm.valueChanges.subscribe((form) => {
      const providedPassword = form.userPassword;
      const providedConfirmPassword = form.confirmUserPassword;

      providedPassword !== providedConfirmPassword
        ? this.registrationForm
            .get('confirmUserPassword')
            ?.setErrors({ notMatched: true })
        : this.registrationForm.get('confirmUserPassword')?.setErrors(null);
    });
  }
}
