import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphWebglComponent } from './graph-webgl.component';

describe('GraphWebglComponent', () => {
  let component: GraphWebglComponent;
  let fixture: ComponentFixture<GraphWebglComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GraphWebglComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GraphWebglComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
