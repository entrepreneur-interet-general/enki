import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MessagesService, Tag } from '../messages.service';

@Component({
  selector: 'app-add-label',
  templateUrl: './add-label.component.html',
  styleUrls: ['./add-label.component.scss']
})
export class AddLabelComponent implements OnInit {
  labelSearch = new FormControl('')
  labels: Array<Tag>
  selectedLabels: Array<Tag>

  constructor(
    private messagesService: MessagesService
  ) {
    // this.labels = this.messagesService.tags
    this.selectedLabels = []
    messagesService.getLabels().subscribe(labels => {
      this.labels = labels
    })
  }

  ngOnInit(): void {
  }

  addLabel(): void {
    this.messagesService.addTag(this.labelSearch.value).subscribe(label => {
      debugger;
      this.messagesService.tags.push(label)
      this.selectLabel(label)
      this.labelSearch.setValue('')
    })
  }

  unselectLabel(): void {

  }

  selectLabel(label): void {
    this.selectedLabels = this.selectedLabels.concat(label)
  }

  getLabels(): void {

  }
}
