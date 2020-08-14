import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {MatSlideToggleChange} from "@angular/material/slide-toggle";
import {CourseService} from "../../services/course/course.service";

@Component({
  selector: 'app-course-watchlist',
  templateUrl: './course-watchlist.component.html',
  styleUrls: ['./course-watchlist.component.css']
})
export class CourseWatchlistComponent implements OnInit {

  constructor(private formBuilder: FormBuilder,
              private courseService: CourseService) { }

  courses = [];
  activeCourses = [{name: 'Teorija informacije', tag: 'tinf', url:'https://www.fer.unizg.hr/predmet/teoinf_b', watch: true},
                   {name: 'Skriptni jezici', tag: 'skriptni', url:'https://www.fer.unizg.hr/predmet/skrjz', watch: true}];
  courseTagList = ['tinf', 'skriptni'];
  urlPrefix = 'https://www.fer.unizg.hr/predmet/';
  courseForm: FormGroup;
  requiredErrorMsg = 'Obavezno polje';
  hovered: number = -1;


  ngOnInit(): void {
    this.courseForm = this.formBuilder.group({
      name: ['', Validators.required],
      tag: [null, Validators.required],
      url: [this.urlPrefix, Validators.required],
      watch: [true, Validators.required]
    })
    this.courseService.getAllCourses().subscribe(response => {
      this.courses = response;
      console.log(this.courses);
    });
  }

  submitForm() {
    if(this.courseForm.valid) {
      this.courseService.saveCourse(this.courseForm.value).subscribe(response => {
        console.log(response);
      });
    }
  }

  toggleChange(event: MatSlideToggleChange) {
    this.courseForm.get('watch').setValue(event.checked);
  }

  hoverStyle(): any {
    return {
            background: 'darkgrey',
            cursor: 'pointer'
          };
  }

}
