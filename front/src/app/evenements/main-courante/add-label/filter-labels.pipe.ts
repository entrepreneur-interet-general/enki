import { Pipe, PipeTransform } from '@angular/core';
import { Label } from '../labels.service';

@Pipe({
  name: 'filterLabels'
})
export class FilterLabelsPipe implements PipeTransform {

  transform(labels: Array<Label>, ...args: any[]): any {
    if(!labels) {
      return [];
    }
    return labels.filter(label => {
      let selectedLabelsUUID = args[1].map(item => item.uuid)
      return label.title.toLowerCase().indexOf(args[0].toLowerCase()) !== -1 && !selectedLabelsUUID.includes(label.uuid)
    });
  }

}
