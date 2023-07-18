import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

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

        setTimeout(() => {
          this.router.navigateByUrl('/auth/login');
        }, 5000); // Redirect after 5s
      },
      error: (response) => {
        this.registrationResponse.message = response.error.detail;
        this.isRegistered = false;
      },
    });
  }

  ngOnInit(): void {
    this.registrationForm.valueChanges.subscribe((form) => {
      this.registrationResponse.message = '';
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
